import anthropic
from dotenv import load_dotenv
load_dotenv() 

## LLM setting 
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=20,
    messages=[
        {
            "role": "user",
            "content": "Test"
        }
    ]
)