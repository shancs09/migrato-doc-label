import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse,Response
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor
import tempfile,os
import shutil
from utils.watsonx_utils import inference_llm_dutch
from utils.pdf_parser import extract_text_by_page, extract_tables_by_page, extract_keywords_and_signals, build_structured_summary
from uuid import uuid4

app = FastAPI()

# CORS setup (to support Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Make sure we have a folder to store previews
PREVIEW_DIR = "previews"
os.makedirs(PREVIEW_DIR, exist_ok=True)


class DocumentLabelResponse(BaseModel):
    filename: str
    document_label: str
    explanation: str
    preview_path: str

def clear_all_previews():
    for filename in os.listdir(PREVIEW_DIR):
        path = os.path.join(PREVIEW_DIR, filename)
        try:
            os.remove(path)
        except Exception as e:
            print(f"[Cleanup] Failed to remove {path}: {e}")

def process_document(file: UploadFile) -> DocumentLabelResponse:
    filename = file.filename
    file_content = file.file.read()

    # Generate a unique ID and save to preview folder
    file_id = str(uuid4())
    preview_filename = f"{file_id}.pdf"
    preview_path = os.path.join(PREVIEW_DIR, preview_filename)
    with open(preview_path, "wb") as f:
        f.write(file_content)

    pages = extract_text_by_page(file_content)
    tables = extract_tables_by_page(file_content)
    signals = extract_keywords_and_signals(pages,tables)
    document_summary = build_structured_summary(pages, tables, signals)
    result = inference_llm_dutch(document_summary)

    label = result.get("label", "Unknown")
    explanation = result.get("explanation", "")

    return {
        "filename": filename,
        "document_label": label.strip(),
        "explanation": explanation.strip(),
        "preview_filename": preview_filename
    }

def process_document_nopreview(file: UploadFile) -> dict:
    filename = file.filename
    file_content = file.file.read()

    pages = extract_text_by_page(file_content)
    tables = extract_tables_by_page(file_content)
    signals = extract_keywords_and_signals(pages,tables)
    document_summary = build_structured_summary(pages, tables, signals)
    result = inference_llm_dutch(document_summary)

    return {
        "filename": filename,
        "document_label": result.get("label", "Unknown").strip(),
        "explanation": result.get("explanation", "").strip(),
        "preview_filename": "" 
    }

@app.post("/label_nopreview")
async def label_documents_nopreview(files: List[UploadFile] = File(...)):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_document_nopreview, files))
    return JSONResponse(content=results)

@app.post("/label")
async def label_documents(files: List[UploadFile] = File(...)):
    clear_all_previews() 
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_document, files))
    return JSONResponse(content=results)

@app.get("/preview/{preview_filename}")
async def preview_file(preview_filename: str):
    path = os.path.join(PREVIEW_DIR, preview_filename)
    return FileResponse(
        path,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{preview_filename}"'}
    )