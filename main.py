import os 
from dotenv import load_dotenv
from openai import OpenAI 
import argparse
import json
from call_function import *
import sys 
load_dotenv()
parser=argparse.ArgumentParser(description='chatbot')
parser.add_argument("user_prompt",type=str,help='user_prompt')
parser.add_argument("--verbose", action="store_true",help="Enable verbose output")
args=parser.parse_args()
#can access args.user_prompt
system_prompt="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
messages=[
    {"role":"system","content":system_prompt},
    {"role":"user","content":args.user_prompt},
]
def main(): 
    api_key=os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    client=OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for _ in range(50):
        response=client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_function,
            temperature=0,
        )
        message=response.choices[0].message
        messages.append(message)
        if response.usage is None :
            raise RuntimeError("API request failed")
        message=response.choices[0].message
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message=call_function(tool_call, verbose=args.verbose)
                    if not result_message["content"]:
                        raise RuntimeError("Empty tool result")
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                    messages.append(result_message)
        else:
            print(message.content)
            return
    print("Error: Maximum iterations reached without a final response.")
    sys.exit(1)
if __name__ == "__main__":
    main()
