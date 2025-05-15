from fetch_reviews import fetch_reviews
from clean_reviews import clean_reviews
from format_for_llm import format_for_llm

def process_professor(prof_name):
    raw_file = fetch_reviews(prof_name)
    cleaned = clean_reviews(raw_file)
    llm_ready_path = format_for_llm(cleaned)
    print(f"Preprocessed LLM input saved at: {llm_ready_path}")

if __name__ == "__main__":
    name = input("Enter professor name: ")
    process_professor(name)
