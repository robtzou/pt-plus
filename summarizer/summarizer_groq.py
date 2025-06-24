
from groq import Groq

client = Groq(api_key = "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")
completion = client.chat.completions.create(
    
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role":"user",
            "content": "How many countries are there in East-Asia?"

        }
    ]
)
print(completion.choices[0].message.content)