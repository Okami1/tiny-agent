import os
import json
import anthropic
from dotenv import load_dotenv


from tools import tools, list_dir, read_file, fetch_url

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def agent_loop():

    print("Welcome to the Claude tiny-agent. Type 'exit' to quit.")
    user_input = input("User: ")

    messages = [
        {"role": "user", "content": user_input},
    ]
    
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        tool_choice={"type": "auto"},
    )
    non_tool_blocks = [block for block in response.content if block.type != "tool_use"]
    tool_blocks = [block for block in response.content if block.type == "tool_use"]
    tool_use_requested = len(tool_blocks) > 0

    messages += [{"role": "assistant", "content": non_tool_blocks}]

    while tool_use_requested:
        for tool_use in tool_blocks:
            print(f"Claude called \"{tool_use.name}\" with {json.dumps(tool_use.input)}")

            if tool_use.name == "list_dir":
                path = tool_use.input.get("path")
                result = list_dir(path)
            elif tool_use.name == "read_file":
                path = tool_use.input.get("path")
                result = read_file(path)
            elif tool_use.name == "fetch_url":
                url = tool_use.input.get("url")
                result = fetch_url(url)
                
            messages += [
                {"role": "assistant", "content": [tool_use]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": str(result),
                        }
                    ],
                },
            ]

        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "auto"},
            messages=messages,
        )
        non_tool_blocks = [block for block in response.content if block.type != "tool_use"]
        tool_blocks = [block for block in response.content if block.type == "tool_use"]
        tool_use_requested = len(tool_blocks) > 0
    
        messages += [{"role": "assistant", "content": non_tool_blocks}]

    final_response = next(block for block in response.content if block.type == "text")
    print(final_response.text)

if __name__ == "__main__":
    agent_loop()
