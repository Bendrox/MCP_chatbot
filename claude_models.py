# import
import os
from typing import Optional
import anthropic
from dotenv import load_dotenv
load_dotenv() 
from typing import Any, Dict, List, Optional


api_key = os.getenv("ANTHROPIC_API_KEY")

class Claude35:
    """
    Model version : claude-3-5-haiku-20241022
    """
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model= "claude-3-5-haiku-20241022"
    
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
class Claude4:
    """
    Model version : claude-sonnet-4-20250514
    """
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
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
    
    def continue_with_history(
        self,
        messages ,
        max_tokens: int = 256,
        tools: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Relance le modèle avec l'historique mis à jour 
        """
        return self.generate_with_tools(messages, max_tokens=max_tokens, tools=tools)
