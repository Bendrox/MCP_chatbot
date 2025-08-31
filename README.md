# MCP Chatbot: Multi-Level Academic Research Assistant

## 🤖 Project Overview

MCP Chatbot is an advanced, multi-level chatbot designed for academic research and paper exploration. Leveraging sophisticated natural language processing techniques, this project provides intelligent interactions with academic content, particularly focusing on arXiv research papers.

## 📚 Key Features

- **Multi-Level Architecture**: 
  - `chatbot_lvl1_tools.py`: Basic chatbot functionality
  - `chatbot_lvl2_mcp_v2.py`: Enhanced interaction capabilities
  - `chatbot_lvl3_multi_mcp.py`: Advanced multi-model processing

- **ArXiv Integration**:
  - `arxiv_tools_4_chatbot.py`: Seamless research paper retrieval and analysis
  - Search and extract information from academic repositories
  - Support for in-depth paper exploration

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
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

- **Level 1 Tools**: Basic chatbot functionalities
- **Level 2 MCP**: Enhanced interaction model
- **Level 3 Multi-MCP**: Advanced multi-model processing
- **ArXiv Tools**: Research paper retrieval and analysis

