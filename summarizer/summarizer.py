import json
import requests
from datetime import datetime
from pathlib import Path
import argparse

# Prompt for summarizing the "all_merged_reviews" text

SUMMARIZE_TEXT_PROMPT = """In 100 hundred words, please focus on personality of the professor, then course structure, and finally any general critiques to watchout for.

Student Feedback:
{text_content}

Summary Paragraph:
"""

# Generate summary using Ollama API
def generate_ollama_summary(text_to_summarize, model="summllama", ollama_url="http://localhost:11434/api/generate", max_summary_tokens=600):
    """
    Generates a summary for the given text using the Ollama API.
    """
    prompt = SUMMARIZE_TEXT_PROMPT.format(text_content=text_to_summarize)
    
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_summary_tokens,
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status() 
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama API at {ollama_url}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from Ollama. Response text: {response.text if 'response' in locals() else 'No response object'}")
    except KeyError:
        print(f"Unexpected response structure from Ollama. 'response' key missing. Response text: {response.text if 'response' in locals() else 'No response object'}")
    
    return "Error generating summary"

# Main processing function for each JSON file
def process_json_and_summarize(input_filepath_str):
    """
    Reads a JSON file, summarizes the "all_merged_reviews" field,
    adds a summarization timestamp, and saves the entire updated JSON structure,
    overwriting any existing summary file with the same derived name.
    """
    input_filepath = Path(input_filepath_str)
    summaries_dir = Path("data/summaries")
    summaries_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(input_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_filepath}")
        return
    except Exception as e:
        print(f"An error occurred while reading {input_filepath}: {e}")
        return

    if "all_merged_reviews" in data:
        original_reviews_text = data["all_merged_reviews"]
        
        if not isinstance(original_reviews_text, str) or not original_reviews_text.strip():
            print(f"Warning: 'all_merged_reviews' in {input_filepath.name} is empty or not a string. Using original content for this field.")
            summary = original_reviews_text 
        else:
            print(f"Summarizing 'all_merged_reviews' for {input_filepath.name}...")
            summary = generate_ollama_summary(original_reviews_text)
        
        data["all_merged_reviews"] = summary
    else:
        print(f"Warning: 'all_merged_reviews' field not found in {input_filepath.name}. This field will not be modified.")

    # Add/update summarization timestamp INSIDE the JSON
    data["date_summarized"] = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct output path WITHOUT timestamp in filename to ensure overwriting
    output_filename = f"{input_filepath.stem}_summary{input_filepath.suffix}" 
    out_path = summaries_dir / output_filename

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Processed file saved (or overwritten): {out_path}")
    except Exception as e:
        print(f"An error occurred while writing the output file {out_path}: {e}")

def format_professor_name_for_filename(name_str):
    """Converts 'Firstname Lastname' to 'Firstname+Lastname'."""
    return name_str.replace("+", "_")

def summarize_single_professor(professor_name_str):
    """
    Finds and processes the JSON file for a single specified professor.
    """
    formatted_name = format_professor_name_for_filename(professor_name_str)
    # Expected input filename pattern: reviews_Firstname+Lastname_llm.json
    filename = f"reviews_{formatted_name}_llm.json"
    input_filepath = Path("data/preprocessed") / filename

    if not input_filepath.exists():
        print(f"Error: Input file not found for professor '{professor_name_str}' (expected at {input_filepath})")
        print("Please ensure the professor's name is correct and the file exists in 'data/preprocessed/'.")
        return

    print(f"\nProcessing single professor: {professor_name_str} (File: {input_filepath.name})...")
    process_json_and_summarize(input_filepath)

def run_summarization_on_all_files():
    """
    Processes all JSON files in the 'data/preprocessed' directory.
    """
    preprocessed_dir = Path("data/preprocessed") 
    
    if not preprocessed_dir.exists():
        print(f"Error: Input directory not found: {preprocessed_dir}")
        print("Please create it and place your JSON files there.")
        return
        
    json_files = list(preprocessed_dir.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {preprocessed_dir}.")
        return

    print(f"Found {len(json_files)} JSON file(s) in {preprocessed_dir}. Starting batch processing...")
    for file_path in json_files:
        print(f"\nProcessing {file_path.name}...")
        process_json_and_summarize(file_path) # This will use the overwrite behavior
    
    print("\nFinished batch processing all files.")

def main():
    parser = argparse.ArgumentParser(
        description="Summarize professor profiles using Ollama. \n"
                    "Processes JSON files from 'data/preprocessed/' and saves summaries to 'data/summaries/'.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--professor", 
        type=str, 
        help="The full name of the professor to summarize (e.g., 'Aric Grossman').\n"
             "The script will look for a file named 'reviews_Firstname+Lastname_llm.json'."
    )
    group.add_argument(
        "--all", 
        action="store_true", 
        help="Summarize all professor profiles in the 'data/preprocessed/' directory."
    )

    args = parser.parse_args()

    if args.professor:
        summarize_single_professor(args.professor)
    elif args.all:
        run_summarization_on_all_files()

if __name__ == "__main__":
    main()