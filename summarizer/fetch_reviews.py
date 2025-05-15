import requests
import json
from pathlib import Path

"Takes the review and puts it into directory 'data/raw"

def fetch_reviews(professor_name: str, save_dir="data/raw"):
    query_name = professor_name.replace(" ", "+")
    url = f"https://planetterp.com/api/v1/professor?name={query_name}&reviews=true"
    response = requests.get(url).json()

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    out_path = f"{save_dir}/reviews_{query_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)
    return out_path
