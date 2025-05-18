import collections
import json
import os
import argparse

def analyze_professor_course_data(professor_data):
    taught_courses_list = professor_data.get("courses", [])
    reviews_list = professor_data.get("reviews", [])

    taught_course_counts = collections.Counter(taught_courses_list)
    unique_courses = sorted(list(taught_course_counts.keys()))

    course_details_summary = {}
    all_reviews_combined = []  # --- CHANGED: track all reviews

    for course_code in unique_courses:
        current_course_stats = {
            "times_taught": taught_course_counts[course_code],
            "num_reviews": 0,
            "total_rating_sum": 0,
            "avg_rating": 0.0,
            "merged_reviews": []
        }

        for review in reviews_list:
            if review.get("course") == course_code:
                current_course_stats["num_reviews"] += 1
                rating = review.get("rating", 0)
                if isinstance(rating, (int, float)):
                    current_course_stats["total_rating_sum"] += rating
                review_text = review.get("review", "").strip()
                if review_text:
                    current_course_stats["merged_reviews"].append(review_text)
                    all_reviews_combined.append(review_text)  # --- CHANGED: collect global reviews

        if current_course_stats["num_reviews"] > 0:
            current_course_stats["avg_rating"] = round(
                current_course_stats["total_rating_sum"] / current_course_stats["num_reviews"], 2
            )

        course_details_summary[course_code] = {
            "times_taught": current_course_stats["times_taught"],
            "num_reviews": current_course_stats["num_reviews"],
            "avg_rating": current_course_stats["avg_rating"],
            "merged_reviews": " ".join(current_course_stats["merged_reviews"])
        }

    # --- CHANGED: Add all merged reviews globally
    return {
        "all_merged_reviews": " ".join(all_reviews_combined),
        "courses": course_details_summary
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze professor course data.")
    parser.add_argument(
        "--filename",
        required=True,
        help="Base name of the JSON file in data/raw (exclude .json)"
    )
    args = parser.parse_args()

    base_filename = args.filename
    input_path = os.path.join("data", "raw", f"{base_filename}.json")
    output_dir = os.path.join("data", "preprocessed")
    output_path = os.path.join(output_dir, f"{base_filename}_llm.json")

    try:
        os.makedirs(output_dir, exist_ok=True)

        with open(input_path, "r") as infile:
            professor_data = json.load(infile)

        summary = analyze_professor_course_data(professor_data)

        with open(output_path, "w") as outfile:
            json.dump(summary, outfile, indent=2)

        print(f"✅ Output saved to: {output_path}")

    except FileNotFoundError:
        print(f"❌ Input file not found: {input_path}")
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format.")
