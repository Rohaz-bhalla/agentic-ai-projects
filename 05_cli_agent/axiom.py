import os
import json
import requests
import subprocess
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

# Initialize the client correctly pointing to Groq
client = OpenAI()

def run_command(cmd: str):
    try:
        # Use subprocess to capture the actual output text
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        return result
    except Exception as e:
        return f"Error executing command: {str(e)}"



available_tools = {
    
    "run_command": run_command
}

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    
    - run_command(cmd: str): Takes a system linux command as string and executes the command on user's system and returns the output from that command
    
    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }

    Example 2:
    START: What is the weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in getting weather of Delhi in India" }
    PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "Great, we have get_weather tool available for this query." }
    PLAN: { "step": "PLAN": "content": "I need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather info about delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The cuurent weather in delhi is 20 C with some cloudy sky." }
    
"""

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step: PLAN, OUTPUT, or TOOL")
    content: Optional[str] = Field(None, description="Your thought or final response")
    tool: Optional[str] = Field(None, description="The name of tool to call")
    input: Optional[str] = Field(None, description="The input for the tool")

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    try:
        user_query = input("\n👉🏻 ")
        message_history.append({"role": "user", "content": user_query})
    
        # Agent Thought Loop
        while True:
            # FIX: Use standard completion, not beta parse, and specify json_object
            response = client.chat.completions.create(
                model="gpt-5-nano",
                response_format={"type": "json_object"},
                messages=message_history
            )
    
            raw_result = response.choices[0].message.content
            
            # Save assistant's raw thought to history
            message_history.append({"role": "assistant", "content": raw_result})
            
            # FIX: Manually parse the JSON and validate it via Pydantic
            try:
                parsed_dict = json.loads(raw_result)
                parsed_result = MyOutputFormat(**parsed_dict)
            except json.JSONDecodeError:
                print(f"❌ Failed to parse JSON. Raw output: {raw_result}")
                break
            except Exception as e:
                print(f"❌ Validation Error: {e}")
                break
    
            if parsed_result.step == "TOOL":
                tool_name = parsed_result.tool
                tool_input = parsed_result.input
                print(f"🛠️  Calling Tool: {tool_name}({tool_input})")
    
                # Execute the tool
                if tool_name in available_tools:
                    output = available_tools[tool_name](tool_input)
                else:
                    output = f"Error: Tool '{tool_name}' not found."
                    
                print(f"👁️  Observation: {output}")
    
                # Feed the observation back as a user role so the AI can "see" it
                message_history.append({
                    "role": "user", 
                    "content": f"OBSERVE: Tool {tool_name} returned: {output}"
                })
                continue # Let the AI process the new information
    
            elif parsed_result.step == "PLAN":
                print(f"🧠 {parsed_result.content}")
                continue
    
            elif parsed_result.step == "OUTPUT":
                print(f"🤖 {parsed_result.content}")
                break # Exit the thought loop and wait for new user input

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        break