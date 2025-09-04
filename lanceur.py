import os
from llm.claude_models import Claude35

chatbots = {
            "1": {
                "name": "Chatbot LvL1 - Outils de base",
                "module": "chatbots.chatbot_lvl1_tools",
                "description": "Basic Chatbot with tools to interact with Arxiv"
            },
            "2": {
                "name": "Chatbot LvL2 - MCP Tools", 
                "module": "chatbots.chatbot_lvl2_mcp_tools",
                "description": "Enhanced Chatbot capabilities with MCP Client - Server (2 tools from arxiv)"
            },
            "3": {
                "name": "Chatbot LvL3 - Multi MCP",
                "module": "chatbots.chatbot_lvl3_multi_mcp", 
                "description": "Advanced Chatbot with multi MCP servers (+ Fetch, Github & filesystem)"
            },
            "4": {
                "name": "Chatbot LvL4 - Advanced",
                "module": "chatbots.chatbot_lvl4",
                "description": "Advanced Chatbot enhanced with prompts & resources"
            }
        }
        

print("-"*30)
print("🤖 Chatbots disponibles")
print("-"*30)

for i , ii in chatbots.items():
    print(i, ii['name'])
    print('└────────', "Description:", ii['description'])
    print("")

print("-"*30)
choice = input("Choisissez une version (numéro): ")

if choice in chatbots:
    os.system(f"python3 -m {chatbots[choice]["module"]}")
    #print(f"python3 -m {chatbots[choice]["module"]}")
