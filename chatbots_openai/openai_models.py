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
    Model version : gpt-5-nano-2025-08-07 - Chat Completions API
    """
    def __init__(self):
        self.client = OpenAI()
        self.model= "gpt-5-nano-2025-08-07"
    
    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_with_tools(self, messages: List[Dict], max_tokens: int = 2000, tools=None):
        """
        Génère une réponse avec support des outils - Chat Completions API
        """
        # Convert MCP tools format to Chat Completions API tools format
        chat_tools = []
        if tools:
            for tool in tools:
                if not isinstance(tool, dict) or "name" not in tool or "description" not in tool or "parameters" not in tool:
                    continue
                
                # Chat Completions API format (standard OpenAI)
                chat_tool = {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                }
                chat_tools.append(chat_tool)
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            tools=chat_tools if chat_tools else None,
            messages=messages,
        )
        return response


class OpenAI_5_mini():
    """
    Model version : 'gpt-5-mini-2025-08-07' - Chat Completions API
    """
    def __init__(self):
        self.client = OpenAI()
        self.model= "gpt-5-mini-2025-08-07"
    
    def generate(self, prompt: str, max_tokens: int = 900) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_with_tools(self, messages: List[Dict], max_tokens: int = 2000, tools=None):
        """
        Génère une réponse avec support des outils - Chat Completions API
        """
        # Convert MCP tools format to Chat Completions API tools format
        chat_tools = []
        if tools:
            for tool in tools:
                if not isinstance(tool, dict) or "name" not in tool or "description" not in tool or "parameters" not in tool:
                    continue
                
                # Chat Completions API format (standard OpenAI)
                chat_tool = {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                }
                chat_tools.append(chat_tool)
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            tools=chat_tools if chat_tools else None,
            messages=messages,
        )
        
        return response
    
    
class OpenAI_5():
    """
    Model version : 'gpt-5-mini-2025-08-07' - Chat Completions API
    """
    def __init__(self):
        self.client = OpenAI()
        self.model= "gpt-5-mini-2025-08-07"
    
    def generate(self, prompt: str, max_tokens: int = 900) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_with_tools(self, messages: List[Dict], max_tokens: int = 2000, tools=None):
        """
        Génère une réponse avec support des outils - Chat Completions API
        """
        # Convert MCP tools format to Chat Completions API tools format
        chat_tools = []
        if tools:
            for tool in tools:
                if not isinstance(tool, dict) or "name" not in tool or "description" not in tool or "parameters" not in tool:
                    continue
                
                # Chat Completions API format (standard OpenAI)
                chat_tool = {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                }
                chat_tools.append(chat_tool)
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_completion_tokens=max_tokens,
            tools=chat_tools if chat_tools else None,
            messages=messages,
        )
        
        return response