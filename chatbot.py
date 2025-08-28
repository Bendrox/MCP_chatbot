## Importing packages
import json

# Loading envir variables
from dotenv import load_dotenv
load_dotenv()

# Importing model
from claude_sonnet import ClaudeSonnet

# arxiv API functions
from arxiv_tools_functions import search_papers, extract_info

PAPER_DIR = "papers" ## Setting local directory name for retreived data


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

## Defining maping functions
mapping_tool_function = {
    "search_papers": search_papers,
    "extract_info": extract_info
}

## Defining functions - tools execution 
def execute_tool(tool_name, tool_args):
    """Execute a tool function from the mapping.

    Args:
        tool_name (str): The name of the tool to execute.
        tool_args (dict): The arguments to pass to the tool function.

    Returns:
        str: The result of the tool execution, formatted as string or JSON.
    """
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
    response = ClaudeSonnet.generate_with_tool(messages,100,tools)
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
                #response = client.messages.create # a remplacer 
                response = ClaudeSonnet.continue_with_history(messages, 
                                                              max_tokens= 100, 
                                                              tools=mapping_tool_function)

## Defining overlall loop for chat/ conversation 
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