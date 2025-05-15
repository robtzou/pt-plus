import os
from pathlib import Path
from summarize_professor import summarize_and_save

PREPROCESSED_DIR = "/summarizer/data/preprocessed"

def summarize_all():
    files = Path(PREPROCESSED_DIR).glob("*.json")
    for file in files:
        summarize_and_save(str(file))

if __name__ == "__main__":
    summarize_all()

