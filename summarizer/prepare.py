import collections
import json
import os
import argparse

"""
Counts the number of times a professor has taught a course.
    Attaches the top three courses to professor profile.
    Attaches the top three traits to descirbe professor.
    Labels the JSON with their name based on file name.
"""

def analyze_professor_course_data(professor_data):
    taught_courses_list = professor_data.get("courses", [])
    reviews_list = professor_data.get("reviews", [])

    taught_course_counts = collections.Counter(taught_courses_list)
    unique_courses = sorted(list(taught_course_counts.keys()))

    course_details_summary = {}
    all_reviews_combined = []

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

    # Get the top three most taught courses
    top_three_courses = sorted(
        course_details_summary.items(),
        key=lambda x: x[1]["times_taught"],
        reverse=True
    )[:3]
    
    # Format the top three courses as a list of dictionaries
    top_courses = [
        {
            "course_code": course_code,
            "times_taught": details["times_taught"],
            "avg_rating": details["avg_rating"]
        }
        for course_code, details in top_three_courses
    ]

    return {
        "name": "",  # This will be filled in the main function
        "all_merged_reviews": " ".join(all_reviews_combined),
        "teaches": top_courses,  # Add the top three courses
        "courses": course_details_summary
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze professor course data.")
    parser.add_argument(
        "--filename",
        help="Base name of the JSON file in data/raw (exclude .json)",
        default=None
    )
    parser.add_argument(
        "--process-all",
        action="store_true",
        help="Process all JSON files in data/raw directory"
    )
    args = parser.parse_args()

    # Create output directory
    output_dir = os.path.join("data", "preprocessed")
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine if processing a single file or all files
    if args.process_all:
        # Process all JSON files in data/raw
        raw_dir = os.path.join("data", "raw")
        try:
            files_processed = 0
            for filename in os.listdir(raw_dir):
                if filename.endswith(".json"):
                    base_filename = filename[:-5]  # Remove .json extension
                    input_path = os.path.join(raw_dir, filename)
                    clean_filename = base_filename.replace("reviews_", "").replace("+","_")
                    output_path = os.path.join(output_dir, f"{clean_filename}.json")
                    
                    try:
                        with open(input_path, "r") as infile:
                            professor_data = json.load(infile)

                        summary = analyze_professor_course_data(professor_data)
                        
                        # Extract the professor's name from the filename
                        professor_name = clean_filename.replace("_", " ")
                        summary["name"] = professor_name

                        with open(output_path, "w") as outfile:
                            json.dump(summary, outfile, indent=2)
                        
                        files_processed += 1
                        print(f"✅ Processed: {filename} -> {clean_filename}.json")
                    
                    except json.JSONDecodeError:
                        print(f"❌ Error: Invalid JSON format in {filename}")
                        continue
            
            print(f"\n✅ Successfully processed {files_processed} files")
            
        except FileNotFoundError:
            print(f"❌ Directory not found: {raw_dir}")
    
    elif args.filename:
        # Process a single file
        base_filename = args.filename
        input_path = os.path.join("data", "raw", f"{base_filename}.json")
        clean_filename = base_filename.replace("reviews_", "").replace("+","_")
        output_path = os.path.join(output_dir, f"{clean_filename}.json")

        try:
            with open(input_path, "r") as infile:
                professor_data = json.load(infile)

            summary = analyze_professor_course_data(professor_data)
            
            # Extract the professor's name from the filename
            professor_name = clean_filename.replace("_", " ")
            summary["name"] = professor_name

            with open(output_path, "w") as outfile:
                json.dump(summary, outfile, indent=2)

            print(f"✅ Output saved to: {output_path}")

        except FileNotFoundError:
            print(f"❌ Input file not found: {input_path}")
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON format.")
    
    else:
        print("❌ Error: Please provide either --filename or --process-all")
        parser.print_help()