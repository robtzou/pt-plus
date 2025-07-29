import requests
import json
import time # Still good to include for general API interaction patterns, though not strictly needed here

print("\nFetching all professors from the PlanetTerp API.")

# API configuration
base_api_url = "https://planetterp.com/api/v1/professors?limit=100&offset=100"

# No need for pagination or semester logic for this specific API endpoint
# The /professor endpoint returns all professors directly.
# No 'per_page' or 'page' parameters for this endpoint.
# No 'semester' parameter for this endpoint.

all_professors = []

try:
    print(f"Making API request to: {base_api_url}")
    response = requests.get(base_api_url)
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

    if 'application/json' in response.headers.get('Content-Type', ''):
        raw_professor_data = response.json()

        if raw_professor_data:
            all_professors.extend(raw_professor_data)
            print(f"Successfully fetched {len(all_professors)} professors.")
        else:
            print("The API returned an empty list of professors.")

    else:
        print(f"Error: Expected 'application/json' but got '{response.headers.get('Content-Type', 'N/A')}'")
        print("Response Body:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")

# --- Save all collected data ---
if all_professors:
    file_output = "planetterp.json"

    with open(file_output, "w", encoding='utf-8') as f:
        json.dump(all_professors, f, indent=4)
    print(f"\nAll collected professor data saved to '{file_output}'")
else:
    print("\nNo professor data was collected. Please check API connectivity.")  