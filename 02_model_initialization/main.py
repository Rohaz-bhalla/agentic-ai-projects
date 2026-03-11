import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role":"system","content":"you are an expert in Maths and only and only answer maths questions avoid LaTex strictly."},
        {"role":"user" , "content":"hey there, who are you ? can you code a python program "},
        {"role":"user" , "content":"hey there, can you solve a + b whole square"}
    ]
)

print(response.choices[0].message.content)