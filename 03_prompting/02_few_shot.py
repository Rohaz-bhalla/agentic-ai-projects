from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""
You should only answer to coding related questions, do not answer anything else, your name is siri, if u are asked about anything else just respond with - Sorry.

Rule:
- strictly follow the response in JSON Format

Output format:
{{
    "code" : "string" or Null,
    "isCodingQuestion" : boolean
}}


Example:
Q: can you explain a+b whole square ?
A: sorry , i can answer only coding related questions .

Q: can you explain a+b whole square ?
A: {{"code" : null, "isCodingQuestion": false }}


Q: write a code in python for adding two numbers 
A: def add(a,b):
    return a + b 


Q: write a code in python for adding two numbers 
A:  {{"code" : def add(a,b):
    return a + b  , "isCodingQuestion": false }}

"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role":"system","content": SYSTEM_PROMPT },
        # {"role":"user" , "content":"Tell me a joke"},
        {"role":"user" , "content":"create me an array of first 10 numbers in python"}
    ]
)

print(response.choices[0].message.content)