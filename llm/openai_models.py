# import
import os
from typing import Optional
import anthropic
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional
from openai import OpenAI

load_dotenv() 

class OpenAI_5_nano():
    """
    Model version : gpt-5-nano-2025-08-07
    """
    def __init__(self):
        self.client = OpenAI()
        self.model= "gpt-5-nano-2025-08-07"
    
    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role":"user", "content":prompt }]
        )
        return msg.content[0].text
    
    def generate_with_tools(self, messages: List[Dict], max_tokens: int = 256, tools=None):
        """
        Génère une réponse avec support des outils
        """
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            tools=tools,
            messages=messages,
        )
        return msg

