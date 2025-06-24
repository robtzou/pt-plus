import csv

# Define the data
deadlines = [
    ["June 2, 2025", "Lab 1", "Lab", "Simple SELECT Queries"],
    ["June 2, 2025", "Quiz 1", "Quiz", "Simple SELECT Queries"],
    ["June 4, 2025", "Lab 2", "Lab", "Multi-Table SELECT Queries"],
    ["June 4, 2025", "Quiz 2", "Quiz", "Multi-Table SELECT Queries"],
    ["June 4, 2025", "Homework 1", "Homework", "SELECT queries, JOINs, UNION"],
    ["June 9, 2025", "Lab 3", "Lab", "Database Design Part One"],
    ["June 9, 2025", "Quiz 3", "Quiz", "Database Design Part One"],
    ["June 9, 2025", "Project Proposal", "Project Deliverable", "Team Project Proposal"],
    ["June 11, 2025", "Lab 4", "Lab", "Database Design Part Two"],
    ["June 11, 2025", "Homework 2", "Homework", "Database Design"],
    ["June 16, 2025", "Lab 5", "Lab", "Data Preparation in Excel"],
    ["June 16, 2025", "Progress Report", "Project Deliverable", "Team Project Progress Report"],
    ["June 18, 2025", "Lab 6", "Lab", "Database Development"],
    ["June 18, 2025", "Homework 3", "Homework", "Database Development"],
    ["June 18, 2025", "Project Standup 1", "Project Deliverable", "Team Project Standup"],
    ["June 23, 2025", "Lab 7", "Lab", "Aggregate Functions"],
    ["June 23, 2025", "Quiz 4", "Quiz", "Aggregate Functions"],
    ["June 25, 2025", "Lab 8", "Lab", "Complex Queries"],
    ["June 25, 2025", "Quiz 5", "Quiz", "Complex Queries"],
    ["June 25, 2025", "Homework 4", "Homework", "Complex Queries"],
    ["June 25, 2025", "Project Standup 2", "Project Deliverable", "Team Project Standup"],
    ["June 30, 2025", "Lab 9", "Lab", "Stored Programs"],
    ["June 30, 2025", "Quiz 6", "Quiz", "Stored Programs"],
    ["June 30, 2025", "Final Project", "Project Deliverable", "Team Project Final Submission"],
    ["July 2, 2025", "Lab 10", "Lab", "More SQL Functions"],
    ["July 2, 2025", "Quiz 7", "Quiz", "More SQL Functions"],
    ["July 7, 2025", "Lab 11", "Lab", "CRUD"],
    ["July 9, 2025", "Lab 12", "Lab", "SQL Interview Prep"],
    ["July 9, 2025", "Project Standup 3", "Project Deliverable", "Team Project Standup"]
]

# Write the data to a CSV file
with open('deadlines.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Assignment", "Type", "Description"])
    writer.writerows(deadlines)