# MCP Chatbot: Multi-Level Academic Research Assistant

## 🤖 Project Overview

This Chatbot is an advanced, multi-tool powered by MCP. It got the ability to retreive academic research and paper exploration from arXiv, building analysis, summarizing papers, save the output locally and retreive local files. 

## 📚 Key Featuress

- **Four chatbots classified by complexity **: 
  - `chatbot_lvl1_tools.py`: Basic Chatbot functionality with tools to interact with arxiv
  - `chatbot_lvl2_mcp_v2.py`: Enhanced Chatbot capabilities with MCP (2 tools from arxiv)
  - `chatbot_lvl3_multi_mcp.py`: Advanced Chatbot with multi MCP servers (adding fetch, Github & filesystem)
  - `chatbot_lvl4.py`: Advanced Chatbot multi-model processing with external MCP servers (adding prompts & resources)

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

- **Chatbot Level 1 Tools**: Basic chatbot functionalities
- **Chatbot Level 2 MCP**: Enhanced interaction model
- **Chatbot Level 3 Multi-MCP**: Advanced multi-model processing
- **ArXiv Tools**: Research paper retrieval and analysis


Author : the Chatbot it self :)