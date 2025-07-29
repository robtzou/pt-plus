import requests
import json
import time
from datetime import datetime

"""
Program to fetch professors from the UMD.io API for the CURRENT semester.
It saves the list of professors active in that semester to a JSON file.
Includes rate limiting to be courteous to the API.
"""

# --- Helper Function for Semester ---
def get_current_umd_semester():
    """
    Determines the current or upcoming UMD semester code (YYYYMM format).
    UMD.io uses 'YYYY01' for Spring, 'YYYY06' for Summer, 'YYYY08' for Fall.
    This logic aims to get the most relevant upcoming or current full semester
    based on the current date.
    """
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month

    # Given current date is July 29, 2025.
    # The most relevant *upcoming* full semester would be Fall 2025 (202508).
    if month >= 8: # August to December: target current year's Fall
        return f"{year}08"
    elif month <= 4: # January to April: target current year's Spring
        return f"{year}01"
    else: # May, June, July: target current year's Summer or upcoming Fall
        # Since it's late July, Fall is typically the next major semester for planning
        return f"{year}08"

current_umd_semester = get_current_umd_semester()
print(f"Determined current UMD semester for API call: {current_umd_semester}")

# --- Main API Request and Data Collection Logic ---

# List to accumulate all professors from all pages for the current semester
current_semester_professors = []

# API configuration
base_api_url = "https://api.umd.io/v1/professors"
items_per_page = 100 # Max items per page as allowed by UMD.io API (often 100)
delay_between_requests = 1.5 # seconds to wait between API calls to respect rate limits

print(f"Fetching professors for the current semester ({current_umd_semester}) from the UMD.io API.")

page_num = 1
while True:
    # Construct the API URL WITH the semester filter
    api_url = f"{base_api_url}?semester={current_umd_semester}&per_page={items_per_page}&page={page_num}"
    print(f"\nMaking API request to: {api_url}")

    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        if 'application/json' in response.headers.get('Content-Type', ''):
            raw_professor_data = response.json()

            if not raw_professor_data:
                print(f"No more professors found on page {page_num} for semester {current_umd_semester}. Stopping further requests.")
                break # Exit loop if an empty list is returned (usually means no more data)

            print(f"Successfully fetched {len(raw_professor_data)} professors from page {page_num}.")

            # Extend the main list with professors from the current page.
            current_semester_professors.extend(raw_professor_data)
            print(f"Total professors collected for {current_umd_semester} so far: {len(current_semester_professors)}")

            page_num += 1 # Move to the next page

            # Implement rate limiting delay
            # Always sleep, unless this was the last page and no more data
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

# --- Save all collected data ---
if current_semester_professors:
    # Use the semester in the filename for clarity
    file_output = f"professors_{current_umd_semester}.json"

    with open(file_output, "w", encoding='utf-8') as f:
        json.dump(current_semester_professors, f, indent=4)
    print(f"\nAll collected professor data for semester {current_umd_semester} saved to '{file_output}'")
else:
    print(f"\nNo professor data was collected for semester {current_umd_semester}. Please check API connectivity or parameters.")