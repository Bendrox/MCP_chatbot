import os

chatbots = {
            "1": {
                "name": "Chatbot LvL1 - Outils de base",
                "file": "./chatbot_lvl1_tools.py",
                "description": "Basic Chatbot with tools to interact with Arxiv"
            },
            "2": {
                "name": "Chatbot LvL2 - MCP Tools", 
                "file": "chatbots/chatbot_lvl2_mcp_tools.py",
                "description": "Enhanced Chatbot capabilities with MCP Client - Server (2 tools from arxiv)"
            },
            "3": {
                "name": "Chatbot LvL3 - Multi MCP",
                "file": "chatbots/chatbot_lvl3_multi_mcp.py", 
                "description": "Advanced Chatbot with multi MCP servers (+ Fetch, Github & filesystem)"
            },
            "4": {
                "name": "Chatbot LvL4 - Advanced",
                "file": "chatbots/chatbot_lvl4.py",
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
    os.system(f"python {chatbots[choice]["file"]}")