from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="google/gemini-3.1-flash-lite-preview",
    max_tokens=100,

    messages = [
        {
            "role" : "user", 
            "content" : [
                {
                    "type" : "text", "text" : "Generate me a caption for this image in a nice structured and professional format"
                },
                {
                    "type" : "image_url",
                    "image_url": {
                        "url": "https://avatars.githubusercontent.com/u/177347071?v=4"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)