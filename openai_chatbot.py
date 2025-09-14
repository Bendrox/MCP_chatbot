from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
import json
import asyncio
import os
import logging

logging.getLogger().setLevel(logging.ERROR)

from chatbots_openai.openai_models import OpenAI_5_nano
from get_token_legifr import get_token

load_dotenv()
llm = OpenAI_5_nano()
max_tokens_param = 5000

class MCP_ChatBot:

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.available_tools = []

    async def connect_to_servers(self): 
        """Connect to all configured MCP servers."""
        try:
            with open("/Users/oussa/Desktop/Github_perso/chatbot_mcp/mcp_server_config/mcp_server_config_openai_FS_LF.json", "r") as file:
                config = json.load(file)
            
            for server_name, server_config in config.get("mcpServers", {}).items():
                url = server_config.get("server", {}).get("url")
                headers = server_config.get("server", {}).get("headers", {})
                
                sse_transport = await self.exit_stack.enter_async_context(
                    sse_client(url, headers=headers)
                )
                
                session = await self.exit_stack.enter_async_context(
                    ClientSession(*sse_transport)
                )
                await session.initialize()
                
                tools = (await session.list_tools()).tools
                print(f"✅ Connected to {server_name} with {len(tools)} tools: {[t.name for t in tools]}")
                
                self.available_tools.extend([{
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                } for tool in tools])
                
        except Exception as e:
            print(f"Error: {e}")

    async def process_query(self, query):
        """Process query with llm.generate_with_tools()."""
        try:
            response = llm.generate_with_tools(
                messages=[{'role': 'user', 'content': query}],
                max_tokens=max_tokens_param,
                tools=self.available_tools
            )
            print(response if isinstance(response, str) else f"Unexpected response: {response}")
        except Exception as e:
            print(f"Error: {e}")

    async def chat_loop(self):
        """Run interactive chat loop"""
        print(f"\nMCP Chatbot Started! ({len(self.available_tools)} tools available)")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                await self.process_query(query)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    chatbot = MCP_ChatBot()
    try:
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()

print(f"Used model: {llm.model}")

if __name__ == "__main__":
    asyncio.run(main())