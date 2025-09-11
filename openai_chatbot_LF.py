from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio
from openai import OpenAI
import os 
import logging

# Réduire les logs de warning pour les notifications SSE
logging.getLogger().setLevel(logging.ERROR)

from llm.openai_models import OpenAI_5_mini, OpenAI_5_nano
from get_token_legifr import get_token

#load_dotenv()
llm = OpenAI_5_nano()
github_barer=os.getenv('github_barer')

## get LegiFrance token 
token=get_token()

# params
max_tokens_param = 5000

class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: dict

class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.sessions: List[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI()
        self.available_tools: List[ToolDefinition] = []
        self.tool_to_session: Dict[str, ClientSession] = {}

    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        """Connect to a single MCP server."""
        try:
            server_info = server_config.get("server", {})
            url = server_info.get("url")
            headers = server_info.get("headers", {})
            
            print(f"Attempting to connect to {server_name} at {url}")
            
            # Create SSE transport
            sse_transport = await self.exit_stack.enter_async_context(
                sse_client(url, headers=headers)
            )
            read, write = sse_transport
            
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()
            self.sessions.append(session)
            
            # List available tools for this session
            try:
                response = await session.list_tools()
                tools = response.tools
                print(f"✅ Connected to {server_name} with {len(tools)} tools:", [t.name for t in tools])

                for tool in tools: 
                    self.tool_to_session[tool.name] = session
                    # Format MCP standard
                    self.available_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    })
            except Exception as tool_error:
                print(f"Connected to {server_name} but failed to list tools: {tool_error}")
                
        except Exception as e:
            print(f"Failed to connect to {server_name}: {str(e)}")

    async def connect_to_servers(self): 
        """Connect to all configured MCP servers."""
        try:
            with open("/Users/oussa/Desktop/Github_perso/chatbot_mcp/mcp_server_config/mcp_server_config_openai_LF.json", "r") as file:
                mcp_server_config_data = json.load(file)
            
            servers = mcp_server_config_data.get("mcpServers", {})
            
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            raise

    async def execute_tool_call(self, tool_name: str, arguments: dict):
        """Execute a tool call via MCP."""
        if tool_name not in self.tool_to_session:
            return f"Tool '{tool_name}' not found"
        
        session = self.tool_to_session[tool_name]
        try:
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else "No result"
        except Exception as e:
            return f"Error executing tool {tool_name}: {e}"
    
    async def process_query(self, query):
        """Process query with tool calling support."""
        messages = [{'role': 'user', 'content': query}]
        
        try:
            # Première requête avec outils disponibles
            response = llm.client.chat.completions.create(
                model=llm.model,
                max_completion_tokens=max_tokens_param,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                } for tool in self.available_tools] if self.available_tools else None
            )
            
            response_message = response.choices[0].message
            
            # Vérifier s'il y a des appels d'outils
            if response_message.tool_calls:
                # Ajouter la réponse de l'assistant aux messages
                messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": response_message.tool_calls
                })
                
                # Exécuter chaque appel d'outil
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # Exécuter l'outil via MCP
                    tool_result = await self.execute_tool_call(tool_name, arguments)
                    
                    # Ajouter le résultat aux messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result)
                    })
                
                # Nouvelle requête avec les résultats des outils
                final_response = llm.client.chat.completions.create(
                    model=llm.model,
                    max_completion_tokens=max_tokens_param,
                    messages=messages
                )
                
                print(final_response.choices[0].message.content)
            else:
                # Pas d'appels d'outils, afficher la réponse directement
                print(response_message.content)
                
        except Exception as e:
            print(f"Erreur lors de l'appel LLM: {e}")
            try:
                response_text = llm.generate(query, max_tokens=max_tokens_param)
                print(f"Réponse sans outils: {response_text}")
            except Exception as fallback_error:
                print(f"Erreur même sans outils: {fallback_error}")

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Close all resources using AsyncExitStack."""
        await self.exit_stack.aclose()

async def main():
    chatbot = MCP_ChatBot()
    try:
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()

print(f"Used model : {llm.model}")

if __name__ == "__main__":
    asyncio.run(main())