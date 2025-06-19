import pdfplumber
import io,re,os,json
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file (if using dotenv for environment variables)
load_dotenv()


def extract_text_by_page(file_bytes: bytes) -> List[str]:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return [page.extract_text() for page in pdf.pages if page.extract_text()]

def extract_tables_by_page(file_bytes: bytes) -> List[List[Dict]]:
    tables = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.append(page_tables if page_tables else [])
    return tables

def extract_keywords_and_signals(pages: List[str],table_flags: List[List[Dict]]) -> Dict:
    # Load and parse keyword map from environment variable
    keyword_signals_raw = os.getenv('KEYWORD_SIGNALS')
    try:
        keyword_signals = json.loads(keyword_signals_raw)
    except Exception as e:
        raise ValueError("Failed to parse KEYWORD_SIGNALS env variable. Ensure it's a valid JSON string.") from e

    signals = {key: 0 for key in keyword_signals}
    signals["currency_symbols"] = 0
    signals["table_pages"] = 0  

    for i, text in enumerate(pages):
        lower_text = text.lower()

        for key, terms in keyword_signals.items():
            signals[key] += sum(1 for term in terms if term in lower_text)

        signals["currency_symbols"] += len(re.findall(r"[$€₹]", text))
        if i < len(table_flags) and table_flags[i]: # Check if page has tables
            signals["table_pages"] += 1

    return signals

# def extract_keywords_and_signals(pages: List[str], keyword_signals: Dict[str, List[str]] = KEYWORD_SIGNALS) -> Dict:
#     signals = {key: 0 for key in keyword_signals}
#     signals["currency_symbols"] = 0

#     for text in pages:
#         lower_text = text.lower()
#         for key, terms in keyword_signals.items():
#             signals[key] += sum(1 for term in terms if term in lower_text)
#         signals["currency_symbols"] += len(re.findall(r"[$€₹]", text))

#     return signals

def build_structured_summary(pages: List[str], table_flags: List[List[Dict]], signals: Dict) -> str:
    summary = []
    for i, page_text in enumerate(pages):
        lines = page_text.strip().split("\n")[:10]  # Limit summary to top lines per page
        summary.append(f"Page {i+1}:\n" + "\n".join(lines))

        if table_flags[i]:
            summary.append("- Contains table(s)")

    # Add heuristic signals
    signal_items = [f"{k}: {v}" for k, v in signals.items() if v > 0]
    signal_str = "\nHeuristic Signals Detected:\n" + ("\n".join(signal_items) if signal_items else "None")

    return "\n\n".join(summary) + signal_str
