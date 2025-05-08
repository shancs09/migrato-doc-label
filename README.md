
# 🧠 Multi-PDF Document Classifier with FastAPI and Streamlit

This project provides a full-stack AI-powered document classification system using **Watsonx**, **FastAPI**, and **Streamlit**. It enables batch uploading of PDF files, intelligent LLM-based labeling, and an interactive UI to view results.

---
## Demo:

<img width="1054" alt="Screenshot 2025-05-08 at 13 30 16" src="https://github.com/user-attachments/assets/d5ceabc9-a60f-401f-b303-3125af7c53bd" />
<img width="1021" alt="Screenshot 2025-05-08 at 13 30 31" src="https://github.com/user-attachments/assets/26b58436-f948-45e9-ae9e-ca63b9c89707" />

## 🗂️ Project Structure

```
.
├── fastapi
│   ├── Dockerfile
│   ├── env_sample
│   ├── main.py
│   ├── previews/
│   ├── requirements.txt
│   └── utils/
│       ├── pdf_parser.py
│       └── watsonx_utils.py
├── llm_instruction.yaml
└── streamlit
    ├── Dockerfile
    ├── env_sample
    ├── requirements.txt
    └── st_main.py
```

---

## 🚀 Features

- 🔍 **Multi-language document classification**
- 📎 **Multi-PDF uploads with bulk classification**
- 📄 **Preview PDFs in-browser**
- 🌐 **FastAPI backend with multithreaded processing**
- 🖥️ **Streamlit frontend with progress feedback**
- ☁️ **Deployable on IBM Cloud Code Engine**

---

## 📦 Setup

### 1. Environment Variables

Copy the sample `.env_sample` in both `fastapi/` and `streamlit/` directories and rename as `.env`.

```bash
cp env_sample .env
```

### 2. FastAPI Requirements

```bash
cd fastapi
pip install -r requirements.txt
```

### 3. Streamlit Requirements

```bash
cd streamlit
pip install -r requirements.txt
```

---

## 🐳 Dockerized Deployment

### Build and Push Docker Images

```bash
# FastAPI
cd fastapi
docker build -t <your-registry>/fastapi-doc-label:latest .
docker push <your-registry>/fastapi-doc-label:latest

# Streamlit
cd ../streamlit
docker build -t <your-registry>/streamlit-doc-label:latest .
docker push <your-registry>/streamlit-doc-label:latest
```

### IBM Cloud Code Engine Deployment

```bash
ibmcloud ce app create --name fastapi-doc-label   --image <your-registry>/fastapi-doc-label:latest   --port 8080

ibmcloud ce app create --name streamlit-doc-label   --image <your-registry>/streamlit-doc-label:latest   --port 8501
```

---

## 📁 Watsonx Prompt Template

The prompt used for classification is defined in `llm_instruction.yaml` and supports auto-detecting languages and JSON-only responses.

---

## 🔧 API Endpoints

- `POST /label`: Classify and store preview
- `POST /label_nopreview`: Classify without storing file
- `GET /preview/{filename}`: Stream preview PDF

<img width="1457" alt="Screenshot 2025-05-08 at 13 29 58" src="https://github.com/user-attachments/assets/0f62fc33-d347-4245-b644-91c418bbd05a" />

---

## 🧼 Housekeeping

Temporary files stored in `fastapi/previews` are cleaned up at runtime to avoid cluttering the filesystem.

---

## 📬 Contact

For issues, please open an [issue on GitHub](https://github.com/your-repo-url/issues).
