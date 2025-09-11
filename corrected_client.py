from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio
from openai import OpenAI
import os
import logging
import requests

# Réduire les logs de warning pour les notifications SSE
logging.getLogger().setLevel(logging.ERROR)

from llm.openai_models import OpenAI_5_mini, OpenAI_5_nano
from get_token_legifr import get_token

load_dotenv()
llm = OpenAI_5_nano()
github_bearer = os.getenv('github_bearer')

# Get LegiFrance token
token = get_token()

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

    async def test_server_connection(self, url: str) -> bool:
        """Test if the MCP server is reachable."""
        try:
            # Test the base URL without /sse
            base_url = url.replace('/sse', '')
            response = requests.get(base_url, timeout=5)
            print(f"✅ Server is reachable at {base_url} (Status: {response.status_code})")
            return True
        except Exception as e:
            print(f"❌ Server not reachable at {url}: {e}")
            return False

    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        """Connect to a single MCP server using SSE (compatible with OpenAI)."""
        try:
            server_info = server_config.get("server", {})
            url = server_info.get("url")
            headers = server_info.get("headers", {})
            
            if not url:
                print(f"❌ No URL specified for {server_name}")
                return
            
            print(f"🔗 Attempting to connect to {server_name} at {url}")
            
            # Test server connectivity first
            if not await self.test_server_connection(url):
                print(f"❌ Cannot connect to {server_name} - server not reachable")
                return
            
            # Create SSE transport (compatible with OpenAI)
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
                    # Format MCP standard compatible with OpenAI
                    self.available_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    })
            except Exception as tool_error:
                print(f"⚠️ Connected to {server_name} but failed to list tools: {tool_error}")
                
        except Exception as e:
            print(f"❌ Failed to connect to {server_name}: {str(e)}")
            print(f"   Make sure the server is running with: python3 legifr_mcp_server_openai.py")

    async def connect_to_servers(self): 
        """Connect to all configured MCP servers."""
        try:
            config_path = "/Users/oussa/Desktop/Github_perso/chatbot_mcp/mcp_server_config/mcp_server_config_openai_LF.json"
            
            if not os.path.exists(config_path):
                print(f"❌ Configuration file not found: {config_path}")
                print("Please create the configuration file or update the path")
                return
            
            with open(config_path, "r") as file:
                mcp_server_config_data = json.load(file)
            
            servers = mcp_server_config_data.get("mcpServers", {})
            
            if not servers:
                print("❌ No servers configured in the configuration file")
                return
            
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
                
        except Exception as e:
            print(f"❌ Error loading server configuration: {e}")

    async def execute_tool_call(self, tool_name: str, arguments: dict):
        """Execute a tool call via MCP."""
        if tool_name not in self.tool_to_session:
            return f"Tool '{tool_name}' not found in available tools: {list(self.tool_to_session.keys())}"
        
        session = self.tool_to_session[tool_name]
        try:
            print(f"🔧 Executing {tool_name} with arguments: {arguments}")
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else "No result returned"
        except Exception as e:
            return f"Error executing tool {tool_name}: {e}"
    
    async def process_query(self, query):
        """Process query with tool calling support (OpenAI compatible)."""
        messages = [{'role': 'user', 'content': query}]
        
        try:
            # Première requête avec outils disponibles (format OpenAI)
            tools_config = None
            if self.available_tools:
                tools_config = [{
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                } for tool in self.available_tools]
                print(f"🛠️ Available tools: {[tool['name'] for tool in self.available_tools]}")
            
            response = llm.client.chat.completions.create(
                model=llm.model,
                max_completion_tokens=max_tokens_param,
                messages=messages,
                tools=tools_config
            )
            
            response_message = response.choices[0].message
            
            # Vérifier s'il y a des appels d'outils
            if response_message.tool_calls:
                print(f"🔧 OpenAI wants to call {len(response_message.tool_calls)} tool(s)")
                
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
                
                print(f"\n💬 Final Answer: {final_response.choices[0].message.content}")
            else:
                # Pas d'appels d'outils, afficher la réponse directement
                print(f"\n💬 Direct Answer: {response_message.content}")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'appel LLM: {e}")
            try:
                response_text = llm.generate(query, max_tokens=max_tokens_param)
                print(f"🔄 Fallback response: {response_text}")
            except Exception as fallback_error:
                print(f"❌ Error even without tools: {fallback_error}")

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\n🤖 MCP Chatbot Started! (OpenAI Compatible)")
        print("Type your queries or 'quit' to exit.")
        print(f"📊 Connected tools: {len(self.available_tools)}")
        
        if self.available_tools:
            print("🛠️ Available tools:")
            for tool in self.available_tools:
                print(f"   - {tool['name']}: {tool['description']}")
        else:
            print("⚠️ No tools available. Make sure your MCP server is running.")
        
        while True:
            try:
                query = input("\n📝 Query: ").strip()
        
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                    
                await self.process_query(query)
                print("\n" + "-"*50)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    async def cleanup(self):
        """Close all resources using AsyncExitStack."""
        await self.exit_stack.aclose()

async def main():
    chatbot = MCP_ChatBot()
    try:
        print(f"🚀 Starting chatbot with model: {llm.model}")
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())