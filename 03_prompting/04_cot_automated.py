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
{"step":"START" | "PLAN" | "OUTPUT" , "content" : "string" }


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

print("\n\n\n")

message_history=[
    {"role":"system", "content":SYSTEM_PROMPT}
]

user_input=input("⏩ ")
message_history.append({"role":"user", "content":user_input})

while True:
    try:
        response=client.chat.completions.create(
            model="gpt-4.1-nano",
            response_format={"type":"json_object"},
            messages=message_history
        )

        raw_result=response.choices[0].message.content
        message_history.append({"role":"assistant", "content":raw_result})

        parsed_result=json.loads(raw_result)

        step_type=parsed_result.get("step")
        content_type=parsed_result.get("content")

        if step_type == "START":
            print("🤖",content_type)
        elif step_type == "PLAN":
            print("🧠", content_type)
        elif step_type == "OUTPUT":
            print("✅", content_type)
            break
        else:
            print("⚠️ unknown step", parsed_result)
            break

    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}\nRaw output was: {raw_result}")
        break
    except Exception as e:
        print(f"An Error occurred {e}")
        break

print("\n\n\n")