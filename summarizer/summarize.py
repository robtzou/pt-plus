import os
import fitz  # PyMuPDF
from docx import Document
import tiktoken
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

def process_text(text, model="gpt-4", chunk_size=1000):
    tokens, encoder = tokenize_text(text, model)
    return [encoder.decode(chunk) for chunk in chunk_tokens(tokens, chunk_size)]

def get_summary_from_chunks(chunks, command):
    combined_text = "\n".join(chunks)
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts deadlines and outputs CSV-friendly data."},
            {"role": "user", "content": f"{command}\n\nContent to summarize:\n{combined_text}"}
        ]
    )
    return response.choices[0].message.content
