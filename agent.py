import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
  model="claude-opus-5",
  max_tokens=1024,
  messages=[{
    "role": "user",
    "content": "Hello, Claude"
  }]
)
for block in message.content:
    if block.type == "text":
        print(block.text)


## TODO: Build: hardcoded system prompt, one tool (list_dir), the while-loop.