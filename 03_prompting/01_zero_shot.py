import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""
You should only answer to coding related questions, do not answer anything else, your name is siri, if u are asked about anything else just respond with - Sorry.
"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role":"system","content": SYSTEM_PROMPT },
        {"role":"user" , "content":"create me an array of first 10 numbers in python"}
    ]
)

print(response.choices[0].message.content)