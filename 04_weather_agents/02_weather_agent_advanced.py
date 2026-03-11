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

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"
    except Exception as e:
        return f"Network error: {str(e)}"
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN, TOOL, and OUTPUT steps.
For every TOOL call, wait for the OBSERVE step which is the output from the called tool.

Rules:
- Strictly Follow the given JSON output format.
- Only run one step at a time.
- The sequence is START -> PLAN(s) -> TOOL (optional) -> OBSERVE (from user) -> OUTPUT.

Output JSON Format:
{ "step": "PLAN" | "OUTPUT" | "TOOL", "content": "thought string", "tool": "tool_name", "input": "input_string" }
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
                model="llama-3.3-70b-versatile",
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