# import
import os
from typing import Optional
import anthropic
from dotenv import load_dotenv
load_dotenv() 

MODEL_NAME = "claude-sonnet-4-20250514"  # remplace par l’ID exact que tu utilises
api_key = os.getenv("ANTHROPIC_API_KEY")


class ClaudeSonnet:
    def __init__(self, model: str = MODEL_NAME):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text