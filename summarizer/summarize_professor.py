import json
import requests
from datetime import datetime
from pathlib import Path

# Prompt with specific attributes
PROMPT_TEMPLATE = """You are an assistant that writes professor reviews.
Summarize the following student feedback into a short TDLR overview that includes these three key aspects: Do not label the paragraph with these aspects just write them like an informal summary.
1. Professor Personality: Describe the professor's teaching style, demeanor, and personal attributes mentioned by students.
2. Course Structure: Explain how the course is organized, including assignments, exams, and teaching methods.
3. Critiques and Compliments: Highlight specific positive feedback and areas for improvement mentioned by students.

Professor: {professor}
Reviews:
{reviews}

Summary:
"""

# Generate summary using Ollama API
def generate_summary(professor_data):
    reviews = "\n- " + "\n- ".join(professor_data["reviews"])
    prompt = PROMPT_TEMPLATE.format(
        professor=professor_data["professor"],
        reviews=reviews
    )
    
    # Using Ollama API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "summllama", # Change to your preferred Ollama model
            "prompt": prompt,
            "max_tokens": 1024,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return "Error generating summary"

# Main summarization function
def summarize_and_save(filepath):
    preprocessed_dir = Path("data/preprocessed")
    summaries_dir = Path("data/summaries")
    summaries_dir.mkdir(parents=True, exist_ok=True)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = generate_summary(data)

    timestamp = datetime.now().strftime("%Y%m%d")
    name_key = data['professor'].replace(" ", "_")
    out_path = summaries_dir / f"{name_key}_{timestamp}.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "professor": data["professor"],
            "summary": summary,
            "date": timestamp
        }, f, indent=2)

    print(f"Summary saved: {out_path}")

# Optional: Run on all files
def summarize_all():
    preprocessed_dir = Path("data/preprocessed")
    for file in preprocessed_dir.glob("*.json"):
        summarize_and_save(file)

if __name__ == "__main__":
    summarize_all()