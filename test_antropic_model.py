#!curl https://api.anthropic.com/v1/messages \
#        --header "x-api-key: REDACTED" \
#        --header "anthropic-version: 2023-06-01" \
#        --header "content-type: application/json" \
#        --data '{"model": "claude-3-7-sonnet-latest", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello, world"}]}'

from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")


client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=10,
    messages=[
        {
            "role": "user",
            "content": "Test"
        }
    ]
)
print(message.content)