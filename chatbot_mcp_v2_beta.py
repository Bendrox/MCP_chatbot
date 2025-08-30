"""
MCP ChatBot — version annotée 

Ce script connecte un modèle Anthropic (Claude) à un serveur MCP via un transport STDIO. 
Le modèle peut appeler les "tools" (outils) exposés par le serveur MCP, 
et le script gère automatiquement les allers-retours :

- l'utilisateur écrit une question,
- le modèle répond soit en texte, soit en demandant d'utiliser un outil (tool_use),
- le client appelle l'outil via  session MCP et renvoie le résultat au modèle,
-  boucle jusqu'à ce que le modèle rende une réponse finale en texte.

`nest_asyncio.apply()` permet d'éviter les erreurs liées à la boucle asyncio déjà en cours.
"""

from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import asyncio


from claude_models import Claude4, Claude35

load_dotenv()

## Initiate 
Claude35= Claude35()

class MCP_ChatBot:
    """Un petit client de chat connecté à un serveur MCP.

    Rôles principaux :
    - Maintenir une session MCP (`self.session`) pour l'appel des tools.
    - Disposer d'un client Anthropic (`self.anthropic`) pour générer les réponses.
    - Exposer au modèle la liste des tools disponibles (`self.available_tools`).
    """

    def __init__(self):
        # Session MCP (initialisée plus tard dans `connect_to_server_and_run`)
        self.session: ClientSession = None
        # Liste des outils au format attendu par Anthropic (nom, description, schéma d'entrée)
        self.available_tools: List[dict] = []

    async def process_query(self, query):
        """Traite une requête utilisateur de bout en bout.
        Étapes :
        1) Envoie la question au modèle
        2) Si le modèle répond par du texte, on l'affiche. Si la réponse est finale, on s'arrête.
        3) Si le modèle demande d'utiliser un outil (tool_use), on l'appelle via MCP,
           puis on renvoie au modèle le résultat (`tool_result`) pour qu'il continue.
        4) On boucle jusqu'à obtention d'un texte final.
        """
        # Historique des messages dans le format Anthropic
        messages = [{'role': 'user', 'content': query}]

        # Premier appel au modèle
        response= Claude35.generate_with_tools(messages=messages,
                                     max_tokens=2000,
                                     tools=self.available_tools)

        # Drapeau de boucle (NB: le nom ombre la méthode, mais reste local)
        process_query = True

        while process_query:
            # On va reconstruire le contenu assistant pour ce "tour" de réponse
            assistant_content = []

            # `response.content` peut contenir plusieurs items (texte, tool_use, etc.)
            for content in response.content:
                if content.type == 'text':
                    # Affiche immédiatement le texte pour donner du feedback à l'utilisateur
                    print(content.text)
                    # Mémorise l'item texte dans le contenu assistant pour le tour courant
                    assistant_content.append(content)

                    # Si la réponse ne contient qu'un seul item texte,
                    # on considère que c'est une réponse finale → on sort de la boucle
                    if len(response.content) == 1:
                        process_query = False

                elif content.type == 'tool_use':
                    # Le modèle demande explicitement l'utilisation d'un outil MCP
                    assistant_content.append(content)

                    # On ajoute au fil des messages ce que l'assistant "vient de dire" (texte + tool_use)
                    messages.append({'role': 'assistant', 'content': assistant_content})

                    # Récupère les infos nécessaires pour l'appel de l'outil
                    tool_id = content.id            # identifiant unique de l'appel côté Anthropic
                    tool_args = content.input       # arguments (dict) à passer au tool
                    tool_name = content.name        # nom de l'outil à appeler

                    print(f"Calling tool {tool_name} with args {tool_args}")

                    # Appel réel de l'outil via la session MCP (transport stdio)
                    # Le résultat renvoyé par MCP (généralement un contenu structuré)
                    result = await self.session.call_tool(tool_name, arguments=tool_args)

                    # On transmet au modèle le résultat de l'outil, en l'emballant comme `tool_result`
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,  # fait le lien avec l'appel `tool_use`
                                "content": result.content  # contenu renvoyé par le serveur MCP
                            }
                        ]
                    })

                    # Nouveau tour : on redemande au modèle quoi faire maintenant qu'il a le résultat
                    response= Claude35.generate_with_tools(messages=messages,
                                     max_tokens=2000,
                                     tools=self.available_tools)

                    # Si cette nouvelle réponse est un unique texte, on l'affiche et on termine
                    if len(response.content) == 1 and response.content[0].type == "text":
                        print(response.content[0].text)
                        process_query = False

    async def chat_loop(self):
        """Boucle interactive en ligne de commande.

        L'utilisateur peut taper une question ou "quit" pour quitter.
        """
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                await self.process_query(query)
                print("\n")

            except Exception as e:
                # Gestion d'erreur simple pour éviter que la boucle ne s'arrête brutalement
                print(f"\nError: {str(e)}")

    async def connect_to_server_and_run(self):
        """Démarre la connexion au serveur MCP (transport STDIO), liste les outils
        et lance la boucle de chat.

        - `command`/`args` décrivent comment lancer votre serveur MCP local.
          Ici on utilise `python mcp_research_server.py` (adaptez selon votre projet).
        - Une fois connecté, on récupère la liste des tools et on la convertit
          au format attendu par le client Anthropic.
        """
        # Paramètres pour démarrer/joindre un serveur MCP via STDIO
        server_params = StdioServerParameters(
            command="python",                      # binaire/commande à exécuter
            args=["mcp_server_research.py"],  # arguments pour lancer votre serveur MCP
            env=None,                           # variables d'env optionnelles pour le serveur
        )

        # `stdio_client` ouvre un canal (lecture/écriture) vers le serveur MCP lancé ci-dessus
        async with stdio_client(server_params) as (read, write):
            # On crée une session de plus haut niveau par-dessus les flux stdio
            async with ClientSession(read, write) as session:
                self.session = session

                # Handshake/initialisation protocolaire
                await session.initialize()

                # Demande la liste des outils exposés par le serveur MCP
                response = await session.list_tools()
                tools = response.tools

                print("\nConnected to server with tools:", [tool.name for tool in tools])

                # On convertit les ToolInfos MCP vers le format tools attendu par Anthropic
                self.available_tools = [{
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema  # schéma JSON des arguments
                } for tool in response.tools]

                # On démarre la boucle d'IO utilisateur
                await self.chat_loop()


async def main():
    """Point d'entrée asynchrone du script."""
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()


if __name__ == "__main__":
    # Lance la boucle asyncio et exécute `main()`
    asyncio.run(main())
