from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="test"
)

print(f"Model version used: {response.model}" )
print(response.output_text)
