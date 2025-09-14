import os
from chatbots_anthropic.claude_models import Claude35

chatbots = {
            "3": {
                "name": "Chatbot LvL3 - Claude Anthropic - Multi MCP",
                "module": "chatbots_anthropic.chatbot_lvl3", 
                "description": "Advanced Chatbot with multi MCP servers (Fetch, Github & filesystem)"
            },
            "4": {
                "name": "Chatbot LvL4 - Claude Anthropic - Advanced",
                "module": "chatbots_anthropic.chatbot_lvl4",
                "description": "Advanced Chatbot enhanced with multi MCP servers, prompts & resources"
            }
        }
        

print("-"*30)
print("🤖 Chatbots disponibles 🤖")
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
