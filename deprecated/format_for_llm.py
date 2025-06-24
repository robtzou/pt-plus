import json
from pathlib import Path

def format_for_llm(cleaned_data, save_dir="data/preprocessed"):
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    name_key = cleaned_data['professor'].replace(" ", "_")
    out_path = f"{save_dir}/{name_key}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)
    return out_path
