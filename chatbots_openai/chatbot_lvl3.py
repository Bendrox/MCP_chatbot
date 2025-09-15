from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
import json
import asyncio
import logging

logging.getLogger().setLevel(logging.ERROR)

from chatbots_openai.openai_models import OpenAI_5_mini

# pas top pour prod...
import subprocess
import atexit
import time

proc = subprocess.Popen(["python3", "local_mcp_servers/mcp_server_legifr_openai.py"])
atexit.register(proc.terminate)
time.sleep(3)  
print("serveur MCP lanched")

load_dotenv()
llm = OpenAI_5_mini()

class MCP_ChatBot:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.available_tools = []
        self.sessions = []

    async def connect_to_servers(self): 
        with open("/Users/oussa/Desktop/Github_perso/chatbot_mcp/mcp_server_config/mcp_server_config_openai_LF.json", "r") as file:
            config = json.load(file)
        
        for server_name, server_config in config.get("mcpServers", {}).items():
            url = server_config.get("server", {}).get("url")
            headers = server_config.get("server", {}).get("headers", {})
            
            sse_transport = await self.exit_stack.enter_async_context(sse_client(url, headers=headers))
            session = await self.exit_stack.enter_async_context(ClientSession(*sse_transport))
            await session.initialize()
            
            self.sessions.append(session)
            tools = (await session.list_tools()).tools
            print(f"✅ Connected to {server_name} with {len(tools)} tools: {[t.name for t in tools]}")
            
            self.available_tools.extend([{
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            } for tool in tools])
        
    async def process_query(self, query):
        messages = [{'role': 'user', 'content': query}]
        
        while True:
            response = llm.generate_with_tools(messages=messages, max_tokens=5000, tools=self.available_tools)
            message = response.choices[0].message
            
            if message.content:
                print(message.content)
                break
                
            elif message.tool_calls:
                print(f"Exécution de {len(message.tool_calls)} outil(s)...")
                
                messages.append({
                    'role': 'assistant',
                    'content': None,
                    'tool_calls': [{'id': tc.id, 
                                    'type': tc.type, 
                                    'function': {'name': tc.function.name, 'arguments': tc.function.arguments}} for tc in message.tool_calls]
                })
                
                for tc in message.tool_calls:
                    tool_name = tc.function.name
                    tool_args = json.loads(tc.function.arguments)
                    print(f"Appel: {tool_name}({tool_args})")
                    
                    result = await self._execute_tool(tool_name, tool_args)
                    print(f"Résultat: {result}")
                    
                    messages.append({'role': 'tool', 'tool_call_id': tc.id, 'content': result})
            else:
                break

    async def _execute_tool(self, tool_name, tool_args):
        for session in self.sessions:
            try:
                result = await session.call_tool(tool_name, arguments=tool_args)
                return result.content[0].text if result.content else "Outil exécuté"
            except:
                continue
        return f"Erreur: outil {tool_name} non trouvé"

    async def chat_loop(self):
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