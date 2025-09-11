# 🤖 MCP Chatbot a Multi‑Level Assistant for Academic and Legal Search  

## 🧭 Overview

This repository contains a set of multi‑tool chatbots (LvL1 → LvL4) powered by GPT-5 models (OpenAI) and/or Claude (Anthropic), enhanced with the Model Context Protocol (MCP). The goal is to provide differet level of assistants and add‑ons that enable:

- Retrieval and analysis of publications (arXiv)
- Synthesis and organization of scientific content
- Access to local resources (file system) and remote resources (Git repositories, HTTP fetch website content)
- Integration of local and remote MCP servers to extend capabilities (prompts, resources)
- To retrieve data from **LégiFrance** with a homemade MCP server. 

## 🎯 Goal

Provide a modular platform with specialized search‑based conversational assistants capable of orchestrating multiple models and tools via MCP and automating tasks related to the collection, summarization, and management of legal and scientific content.

## 🧩 Chatbot Levels 

- **chatbot\_lvl1** — Basic chatbot with local tools to interact with arXiv.
- **chatbot\_lvl2** — A chatbot with a single MCP server (with arXiv tools).
- **chatbot\_lvl3** — Enhanced chatbot using multiple MCP servers (filesystem, fetch, Git, research).
- **chatbot\_lvl4** — Advanced chatbot using external MCP servers, plus prompts and local resources.
- **chatbot\_lvl5** — In development - Advanced chatbot using external MCP servers, plus prompts and local resources.

## 📁 Repository Structure (top‑level)

- `chatbot_lvl1_tools/` — Basic tools for the chatbot (e.g., arXiv interaction).
- `chatbot_ouputs/` — (probable) directory for storing chatbot outputs.
- `chatbots/` — Chatbot implementations (different levels/variants) with Claude (Anthropic).
- `chatbots_openai/` — Specific integrations and agents with OpenAI’s GPT‑5.
- `llm/` — Wrappers and utilities for LLMs (pre/post‑processing, prompts).
- `local_mcp_servers/` — Configurations/launchers for local MCP servers (filesystem, research, Git…).
- `mcp_server_config/` — Configuration files for MCP servers in use.
- `notebooks/` — Jupyter notebooks for exploration and demos.
- `retreived_arxiv_papers/` — Collection of papers retrieved for testing/examples.
- `requirements.txt` — Python dependencies.
- `docker-compose.yml` + `Dockerfile` — SSE proxy + filesystem MCP server (for OpenAI filesystem).

## 🏗️ Project Architecture

- `lanceur.py` — CLI launcher to run a chatbot version (LvL1 → LvL4)
- `chatbots/`
  - `chatbot_lvl1_tools.py` — Local chatbot with Python tools (arXiv)
  - `chatbot_lvl2_mcp_tools.py` — Chatbot + 1 MCP server (research)
  - `chatbot_lvl3_multi_mcp.py` — Chatbot with multiple MCP servers (filesystem, fetch, Git, research)
  - `chatbot_lvl4.py` — As LvL3, with MCP prompts and resources management
- `chatbots_openai/`
  - `chatbot_lvl3.py` — LvL3 variant using OpenAI APIs
- `chatbot_lvl1_tools/`
  - `arxiv_tools_4_chatbot.py` — Local implementations of arXiv tools
- `local_mcp_servers/`
  - `mcp_server_research.py` — MCP “research” server (arXiv tools)
  - `mcp_server_research_lvl4.py` — Same + resources (`papers://…`) + `generate_search_prompt` prompt
- `mcp_server_config/`
  - `mcp_server_config.json` — MCP server config for LvL2/LvL3
  - `mcp_server_config_lvl4.json` — Config for LvL4 (including resources/prompts)
- `llm/`
  - `claude_models.py` — Anthropic wrappers (Claude 3.5/4)
  - `openai_models.py` — OpenAI wrappers (GPT‑5 / 5‑nano / 5‑mini)
- `notebooks/`
  - `explore.ipynb`, `openai_mcp_chat.ipynb` — Demonstrations
- `chatbot_ouputs/` — Example outputs (MCP summaries)

## 🔌 MCP Servers & Integrations

- **ArXiv** (in `arxiv_tools_4_chatbot.py`): retrieve and analyze research papers; search and extract information from academic repositories; support in‑depth exploration.
- **Filesystem**: secure file operations with configurable access controls.
- **GitHub**: tools to read, search, and manipulate Git repositories.
- **Prompts**: search for papers, extract and organize information, then produce comprehensive summaries.
- **Resources**: access to `papers://folders` (papers retrieved from arXiv).

### 🧰 Resources & Prompting (LvL4)

- **Resources (from **``**)**
  - `papers://folders` → list available topics
  - `papers://{topic}` → details of papers for a topic
- **Chat commands**
  - `@folders` → show available folders
  - `@{topic}` → show papers of a given topic
  - `/prompts` → list available prompts
  - `/prompt <name> arg1=val1 …` → execute a prompt, then continue the conversation

## ⚙️ How It Works — by Level

**LvL1 — Local tools (no MCP)**

- Tools: `search_papers(topic, max_results)`, `extract_info(paper_id)`
- Flow: the LLM selects a tool → the local function runs → results are returned to the model → final answer is generated.

**LvL2 — One MCP server (research)**

- The client starts a local MCP server (arXiv tools) over stdio.
- The LLM calls tools exposed by the server via MCP.

**LvL3 — Multi‑MCP**

- Connects to multiple servers: filesystem, fetch, Git, research.
- Maps each tool name to the corresponding server session.

**LvL4 — MCP Prompts & Resources**

- Adds prompt listing/usage and resource listing/usage to the above.

## 🚀 Getting Started

### 🧰 Prerequisites

- Python **3.13.2**
- Install required libraries (in requirements.txt)
- OpenAI and Claud Anthropic keys
- LegiFrance Ids & keys

### 🛠️ Installation

*In progress*

## ▶️ Usage

*In progress*


## 🔗 Compatibility for OpenAI models

- The OpenAI API can connect to MCP servers as tools (`"type": "mcp"`) in `responses.create` calls **only for remote servers** (HTTP/SSE) via `server_url`; **stdio is not supported** there.
- For **local MCP servers ( running with stdio)** such as filesystem and Git, docker and ngrok have been used to simulate a distant HTTP/SSE connection. 

## Proprietary code

- The homemade MCP server for LegiFrance "remote_legifr_mcp_server.py" is not shared in the github repo. This will have the impact of depriving the chatbot of access to Legifrance content. 

## 🗺️ Roadmap / To‑Do

- Enhance code and integrations.
- Unify output folders (`retreived_arxiv_papers` vs `papers`) or document the mapping.
- Add automated tests and linting.
- Provide an initialization script (make/uv/poe) + export examples.
- Make the MCP config path configurable (`MCP_SERVER_CONFIG` env, CLI flag, or class variable).
- Adjust OpenAI model names to the versions available at runtime.
- Explore related topics: OpenAI Agents SDK, Microsoft Learn MCP Server, Azure AI Foundry Agent Service.
- explore other capabilities offered by Docker for mcp , cloudflare and GCP.

## ✍️ Author

OB

