
import requests
import json
from datetime import datetime

"""
Program to find the most recent professors for a given course.
"""

# find year month for api call.
current_datetime = datetime.now()
year = current_datetime.year
month = current_datetime.month

def semester():
    # find the right semester to pull
    fall   = f"{year}08"
    spring = f"{year}04"

    if   month in range(5,8):
        fall   = f"{year}08"
        return fall
    elif year  in range(9,4):
        return spring 

current_semester = semester()

def course():
    # user input of what course to select
    pass

selected_course = "p"

query = "response"

response = requests.get(f"https://api.umd.io/v1/courses")

# Check if the response is successful and has a content type of application/json
if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
    professorReviews = response.json()

    file_output = f"{query}_{current_semester}.json"

    with open(file_output, "w", encoding='utf-8') as f:
        json.dump(professorReviews, f, indent=4)
else:
    print(f"Error: API returned status code {response.status_code} and content type {response.headers['Content-Type']}")
    print(response.text)