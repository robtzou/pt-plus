import requests
import json

# Replaces space for '+'
professorName = input("Please enter professor name for query: ")
professorNameQuery = professorName.replace("\u0020", "+")
professorReviews = requests.get(f"https://planetterp.com/api/v1/professor?name={professorNameQuery}&reviews=true").json()

directory = "/home/bobby/documents/planetterp-summarizer"
file_output = f"reviews_{professorNameQuery}.json"

with open(file_output, "w", encoding='utf-8') as f:
    json.dump(professorReviews, f, indent=2)