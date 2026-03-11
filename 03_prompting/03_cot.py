from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""

you are an expert AI Assistant in resolving user queries using chain of thought. 

you work on START, PLAN and OUTPUT steps 

you need to first PLAN what needs to be done . The PLAN can be multiple steps.

once you think enough PLAN has been done , finally you can give the OUTPUT

Rules :
- strictly follow the given JSON output format 
- only run one step at a time 
- the sequence of step is START (where user gives an input), PLAN(that can be multiple 
    times ) and finally the OUTPUT (which is going to be displayed to the user )
-Strictly do not use LaTex

Output JSON Format :
{"step":"START" | "PLAN" | "OUTPUT" , "Content" : "string" }


Example :
START : can you solve 2 + 3 * 5 / 10
PLAN : {"step" : "PLAN":"content": " seems like user is interested in maths problem" }
PLAN : {"step" : "PLAN":"content": " looking at the problem , we should solve this using BODMAS method "}
PLAN : {"step" : "PLAN":"content": " yes , the BODMAS is correct thing to be done here" }
PLAN : {"step" : "PLAN":"content": " first, we must multiply 3 * 5 which is 15 " }
PLAN : {"step" : "PLAN":"content": " no the new equation is 2 + 15 /10 " }
PLAN : {"step" : "PLAN":"content": " we must perform divide that is 15/10 = 1.5 "}
PLAN : {"step" : "PLAN":"content": " now the equation is 2 + 1.5 " }
PLAN : {"step" : "PLAN":"content": " now finally lets perform the add" }
PLAN : {"step" : "PLAN":"content": " great, we have finally solved and left with the answer as 3.5"}
OUTPUT : {"step": "OUTPUT": " content" : "3.5" }

"""

response=client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"Hey, there write me a code for adding two numbers in js"},

        # manually keep adding messages to the history
        {"role":"assistant", "content": json.dumps(
            {"step":"START","Content":"User is requesting a JavaScript code snippet to add two numbers."}
        )},

        {"role":"assistant", "content": json.dumps(
            {"step": "PLAN", "Content": "I need to outline the basic structure of a JavaScript function that takes two numbers as inputs."}
        )},
        
        {"role":"assistant", "content": json.dumps(
            {"step": "PLAN", "Content": "The function should include parameters for the two numbers and return their sum."}
        )},

        {"role":"assistant", "content": json.dumps(
            {"step": "PLAN", "Content": "I can present the code in a readable format for the user."}
        )},

    ]
)

print(response.choices[0].message.content)