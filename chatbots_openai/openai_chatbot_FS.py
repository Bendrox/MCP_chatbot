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
#llm = OpenAI_5_mini()
github_barer=os.getenv('github_barer')

## get LegiFrance token 
token=get_token()

# params
max_tokens_param= 5000

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
            
            # Create SSE transport (tous vos serveurs sont SSE)
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
            # Continue with other servers instead of failing completely

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
    
    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        
        try:
            response_text = llm.generate_with_tools(messages=messages,
                                                   max_tokens=max_tokens_param,
                                                   tools=self.available_tools)
            
            if isinstance(response_text, str):
                print(response_text)
            else:
                print(f"Type de réponse inattendu: {type(response_text)}")
                print(f"Contenu: {response_text}")
                
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
        """ close all resources using AsyncExitStack."""
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