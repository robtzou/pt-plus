import csv
import requests
import json
from pathlib import Path

def fetch_reviews(professor_name: str, save_dir="data/raw"):
    query_name = professor_name.replace(" ", "+")
    url = f"https://example.com/api/reviews?prof={query_name}"  # Replace with real API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        filename = Path(save_dir) / f"{professor_name.replace(' ', '_')}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    else:
        print(f"Failed to fetch reviews for {professor_name}")

def load_name_queue(csv_path: str):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row['first_name'], row['last_name']) for row in reader]

if __name__ == "__main__":
    name_queue = load_name_queue("names.csv")
    for first, last in name_queue:
        fetch_reviews(f"{first} {last}")
