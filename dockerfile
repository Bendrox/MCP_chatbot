FROM node:20-alpin

# Installe le proxy SSE et le serveur filesystem
RUN npm i -g mcp-proxy@latest @modelcontextprotocol/server-filesystem@latest

WORKDIR /app
ENV PORT=8000
ENV ROOT=/workdir_filesystem

EXPOSE 8000

# Lance le proxy SSE qui spawn le serveur filesystem (stdio)
# NB: mcp-server-filesystem attend des dossiers autorisés en ARGs
CMD ["sh","-lc","mcp-proxy mcp-server-filesystem ${ROOT} --port ${PORT} --server sse"]