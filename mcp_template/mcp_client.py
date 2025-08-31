from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
# Necessary classes to etablish co to our MCP server
# here param to show to client how to lanch server
server_params = StdioServerParameters(
    command="python3",  # Executable
    args=["run mcp_research_server.py"],  # Command line arguments
    env=None,  # Optional environment variables
)

async def run():
    # Launch the server as a subprocess & returns the read and write streams
    # read: the stream that the client will use to read msgs from the server
    # write: the stream that client will use to write msgs to the server
    async with stdio_client(server_params) as (read, write):  # injection des parametres + etablish co as a sub param
        # the client session is used to initiate the connection 
        # and send requests to server 
        async with ClientSession(read, write) as session: # access to underlying co to have access to methods/functions
            # Initialize the connection (1:1 connection with the server)
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # will call the chat_loop here
            # ....
            
            # Call a tool: this will be in the process_query method
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})


if __name__ == "__main__":
    asyncio.run(run())