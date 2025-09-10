# MCP Chatbot: Multi-Level Academic Research Assistant

## 🤖 Project Overview

This Chatbot is a multi-tool Chatbot powered OpenAI and Claud (Antropic) and MCP. 
Depending on the version and the choosen model, it got the ability to retreive academic research and paper  from arXiv, summarizing papers, retreive local files, save the output locally and make some git actions. 

## 📚 Key versions of the Chatbot

- **Four chatbots classified by complexity **: 
  - `chatbot_lvl1`: Basic Chatbot functionality with tools to interact with arxiv
  - `chatbot_lvl2`: Enhanced Chatbot capabilities with MCP (2 tools from arxiv)
  - `chatbot_lvl3`: Advanced Chatbot with multi MCP servers (adding fetch, Github & filesystem)
  - `chatbot_lvl4`: Advanced Chatbot multi-model processing with external MCP servers (adding prompts & resources)

- **MCP servers Integration**:

  - Arxiv in `arxiv_tools_4_chatbot.py`: Seamless research paper retrieval and analysis, to Search and extract information from academic repositories, Support for in-depth paper exploration
  - filesystem : Secure file operations with configurable access controls
  - Github : Tools to read, search, and manipulate Git repositories
  - Prompts: Search for papers, extract and organize the information then Provide a comprehensive summary
  - Resources: give access to "papers://folders" (papers retreived from Arxiv )

## 🚀 Getting Started

### Prerequisites

- Python Python 3.13.2
- Required libraries (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Bendrox/MCP_chatbot.git
   cd MCP_chatbot
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Usage

### Basic Usage

```python
from chatbot_lvl2_mcp_v2 import MCPChatbot

# Initialize the chatbot
chatbot = MCPChatbot()

# Start interaction
response = chatbot.process_query("Tell me about recent AI research")
print(response)
```

## 🌟 Components

to do 

## Compatibility 

Important a noter ! 
-	L’API d’OpenAI peut se connecter à des MCP (Model Context Protocol) servers en tant qu’outils ("type": "mcp") dans les appels responses.create. Mais uniquement avec serveurs distants (HTTP/SSE) sont supportés → server_url.
-	Pour serveurs locaux (stdio, ex. filesystem, research, git), il faut utiliser le Agents SDK (qui sait lancer les processus avec command / args).
Travail à faire : 
•	OpenAI Agents SDK


Author : the Chatbot it self :)