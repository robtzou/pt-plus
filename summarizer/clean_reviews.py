import json

def clean_reviews(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    professor = data.get("name", "Unknown")
    reviews = [r["review"] for r in data.get("reviews", []) if r.get("review")]

    cleaned_reviews = [r.strip().replace("\n", " ") for r in reviews]
    return {
        "professor": professor,
        "reviews": cleaned_reviews
    }
