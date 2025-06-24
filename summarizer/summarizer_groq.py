import os
from groq import Groq

"""
Currently aiming to take pdf to CSV for G-Calendar

"""
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

with open("token_output.txt", "r", encoding="utf-8") as f:
    syll = f.read()

command = "Find all deadlines and display them during the class time in CSV format for Calendar. Attach information to each deadline and assignment."

completion = client.chat.completions.create(
    
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that follows the user's instructions precisely and summarizes content based on the given command."
        },
        {
            "role": "user",
            "content": f"{command}\n\nContent to summarize:\n{syll}"
        }
    ]
)
print(completion.choices[0].message.content)