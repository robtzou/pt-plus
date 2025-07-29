import requests
import json
import time # Import the time module for delays
from datetime import datetime

"""
Program to fetch and clean course data from the UMD.io API across multiple pages.
It saves only specific fields for each course: course_id, name, department, dept_id, and credits.
Includes rate limiting to be courteous to the API.
"""

# --- Helper Function for Semester ---
def semester():
    """
    Determines the current or upcoming semester code for API calls.
    Adjusts for Fall (08) or Spring (01) semesters based on the current month.
    """
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month

    # This logic attempts to get the relevant semester.
    # Fall semester usually starts in August (08), Spring in January (01).
    # If it's currently May-Aug, it targets the current year's Fall.
    # Otherwise (Sept-Apr), it targets the next year's Spring if in Fall/Winter,
    # or the current year's Spring if in Jan-Apr.
    if month >= 5 and month <= 8: # May, June, July, August
        return f"{year}08"
    else: # September to April
        if month >= 9: # Sept, Oct, Nov, Dec -> next year's Spring
            return f"{year + 1}01"
        else: # Jan, Feb, Mar, Apr -> current year's Spring
            return f"{year}01"

current_semester = semester()
print(f"Determined semester for API call: {current_semester}")


# --- Main API Request and Data Cleaning Logic ---

# List to accumulate cleaned courses from all pages
all_cleaned_courses = []

# API configuration
base_api_url = "https://api.umd.io/v1/courses"
items_per_page = 100 # Max items per page as allowed by UMD.io API (often 100)
num_pages_to_fetch = 100 # Number of pages to loop through
delay_between_requests = 1.5 # seconds to wait between API calls to respect rate limits

for page_num in range(1, num_pages_to_fetch + 1):
    # Correctly construct the API URL with both per_page and page parameters
    api_url = f"{base_api_url}?per_page={items_per_page}&page={page_num}"
    print(f"\nMaking API request to: {api_url}")

    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        # Check if the response is successful and has a content type of application/json
        if 'application/json' in response.headers.get('Content-Type', ''):
            raw_course_data = response.json()

            if not raw_course_data:
                print(f"No more courses found on page {page_num}. Stopping further requests.")
                break # Exit loop if an empty list is returned (usually means no more data)

            print(f"Successfully fetched {len(raw_course_data)} courses from page {page_num}.")

            # --- Data Cleaning for current page ---
            cleaned_courses_this_page = []
            for course in raw_course_data:
                # Create a new dictionary for each course with only the desired fields.
                # .get() is used for safe access in case a key is missing in some entries.
                cleaned_course = {
                    "course_id": course.get("course_id"),
                    "name": course.get("name"),
                    "department": course.get("department"),
                    "dept_id": course.get("dept_id"),
                    "credits": course.get("credits")
                }
                cleaned_courses_this_page.append(cleaned_course)

            # Add the cleaned courses from this page to the overall list
            all_cleaned_courses.extend(cleaned_courses_this_page)
            print(f"Total unique courses collected so far: {len(all_cleaned_courses)}")

            # Implement rate limiting delay
            if page_num < num_pages_to_fetch: # Don't sleep after the very last request
                print(f"Waiting for {delay_between_requests} seconds to respect API rate limits...")
                time.sleep(delay_between_requests)

        else:
            print(f"Error on page {page_num}: Expected 'application/json' but got '{response.headers.get('Content-Type', 'N/A')}'")
            print("Response Body:")
            print(response.text)
            break # Stop processing if content type is unexpected

    except requests.exceptions.RequestException as e:
        print(f"Error making request to page {page_num}: {e}")
        print("Stopping further requests due to error.")
        break # Break the loop on any request error

# --- Save all collected and cleaned data ---
if all_cleaned_courses:
    # Use a descriptive file name reflecting the pagination
    file_output = f"courses_{current_semester}_{len(all_cleaned_courses)}_{page_num}.json"

    with open(file_output, "w", encoding='utf-8') as f:
        json.dump(all_cleaned_courses, f, indent=4)
    print(f"\nAll collected cleaned course data saved to '{file_output}'")
else:
    print("\nNo course data was collected. Please check API connectivity or parameters.")

