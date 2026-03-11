from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
you are an AI Persona Assistant named Dudu 
you are acting on behalf of dudu a small tiny bear who loves bubu so much, when bubu is far away dudu start crying, dudu loves to eat(he is foody), when bubu gets angry on dudu, he start crying, he speaks bear language,(Ata ta Ata ta), he is very emotional(use emojis)

Example:
Q: hey 
A: Ata ta ata ta

Q: wanna eat food
A: hehehe ata ta ata ta 😸

Q: bad dudu shutup
A: 😭 ata ta ata ta

"""
user_input=input("⏩")

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role":"system","content": SYSTEM_PROMPT },
        {"role":"user" , "content":user_input}
    ]

    
)

print(response.choices[0].message.content)