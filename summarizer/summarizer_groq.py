import os
import fitz  # PyMuPDF for PDFs
from docx import Document  # For DOCX files
import tiktoken
from groq import Groq

"""
Currently aiming to take pdf to CSV for a calendar.
"""
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

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

syll = input("Paste fileID as shown in directory.")
chunks = process_syllabus(f"{syll}")

command = "Find all deadlines and display them during the class time in CSV format for Calendar. Attach information to each deadline and assignment."

completion = client.chat.completions.create(
    
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that follows the user's instructions precisely and summarizes content based on the given command."
        },
        {
            "role": "user",
            "content": f"{command}\n\nContent to summarize:\n{syll}"
        }
    ]
)
print(completion.choices[0].message.content)