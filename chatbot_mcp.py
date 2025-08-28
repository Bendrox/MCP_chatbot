## Importing packages & loading env var
import json
import os
from typing import List
from dotenv import load_dotenv
import arxiv # pour l’API d’arXiv.org: dépôt d’articles scientifiques

# loading env variables
from dotenv import load_dotenv
load_dotenv()

# importing model
from claude_sonnet_4 import client, message


## Setting local directory name for retreived data
PAPER_DIR = "papers"

## Defining model functions 
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
        
    Returns:
        List of paper IDs found in the search
    """

    # Use arxiv to find the papers 
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    
    return paper_ids

def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
 
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."


## Setting tools & mapping
tools = [
    {
        "name": "search_papers",
        "description": "Search for papers on arXiv based on a topic and store their information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to search for"
                }, 
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to retrieve",
                    "default": 5
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "extract_info",
        "description": "Search for information about a specific paper across all topic directories.",
        "input_schema": {
            "type": "object",
            "properties": {
                "paper_id": {
                    "type": "string",
                    "description": "The ID of the paper to look for"
                }
            },
            "required": ["paper_id"]
        }
    }
]

mapping_tool_function = {
    "search_papers": search_papers,
    "extract_info": extract_info
}

## Defining functions - tools execution 
def execute_tool(tool_name, tool_args):
    
    result = mapping_tool_function[tool_name](**tool_args)

    if result is None:
        result = "The operation completed but didn't return any results."
        
    elif isinstance(result, list):
        result = ', '.join(result)
        
    elif isinstance(result, dict):
        # Convert dictionaries to formatted JSON strings
        result = json.dumps(result, indent=2)
    
    else:
        # For any other type, convert using str()
        result = str(result)
    return result

## Defining functions - chating & wrapping  

def process_query(query):
    # Étape 1 — ENVOYER LA QUESTION AU MODÈLE (avec outils activés)
    # 1.1 Préparer l'historique avec le message utilisateur
    messages = [{'role': 'user', 'content': query}]
    
    # 1.2 Premier appel au modèle : il peut répondre en texte
    #     OU demander d'utiliser un outil (tool_use)
    response = client.messages.create(
        max_tokens=2024,
        model='claude-3-7-sonnet-20250219',
        tools=tools,
        messages=messages
    )
    keep_looping = True

    # Étape 4 — BOUCLE JUSQU’À LA RÉPONSE FINALE
    while keep_looping:
        assistant_content = []  # contiendra le texte + éventuels tool_use de CE tour

        # Étape 2 — LIRE/INTERPRÉTER LA RÉPONSE DU MODÈLE
        for content in response.content:
            if content.type == 'text':
                # 2.1 Cas "texte direct" : on affiche le texte
                print(content.text)
                assistant_content.append(content)

                # 4.1 Si la réponse ne contient QUE du texte (pas de tool_use),
                #     on peut s'arrêter : réponse finale obtenue
                if len(response.content) == 1:
                    keep_looping = False
            
            elif content.type == 'tool_use':
                # Étape 3 — LE MODÈLE DEMANDE UN OUTIL
                assistant_content.append(content)

                # 3.1 On enregistre côté assistant ce que le modèle vient de dire
                #     (texte éventuel + demande d'outil) dans l'historique
                messages.append({'role': 'assistant', 'content': assistant_content})
                
                # 3.2 Extraire les infos d'appel d'outil
                tool_id = content.id
                tool_args = content.input
                tool_name = content.name
                print(f"Calling tool {tool_name} with args {tool_args}")
                
                # 3.3 Exécuter l'outil localement et récupérer le résultat
                result = execute_tool(tool_name, tool_args)

                # 3.4 Retourner ce résultat au modèle sous forme de "tool_result"
                #     (rôle 'user' selon la convention Anthropic)
                messages.append({
                    "role": "user", 
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        }
                    ]
                })

                # 3.5 Relancer le modèle avec l'historique mis à jour
                response = client.messages.create

## Defining loop for chat

def chat_loop():
    print("Type your queries or 'quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break
            process_query(query)
            print()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    chat_loop()