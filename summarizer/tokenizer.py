import os
import fitz  # PyMuPDF for PDFs
from docx import Document  # For DOCX files
import tiktoken

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def tokenize_text(text, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    return enc.encode(text), enc

def chunk_tokens(tokens, chunk_size=1000, overlap=100):
    chunks = []
    i = 0
    while i < len(tokens):
        chunks.append(tokens[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

def process_syllabus(file_path, model="gpt-4", chunk_size=1000):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type.")

    tokens, encoder = tokenize_text(raw_text, model)
    token_chunks = chunk_tokens(tokens, chunk_size)

    return [encoder.decode(chunk) for chunk in token_chunks]

# Example usage
if __name__ == "__main__":
    chunks = process_syllabus("INST327 Summer 2025 Syllabus.pdf")  # or .docx
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n{chunk[:5000]}...")  # Truncated for display
