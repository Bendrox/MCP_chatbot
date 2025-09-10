from mcp.server.fastmcp import FastMCP
from zoneinfo import ZoneInfo
from datetime import datetime
from fastmcp import Client

mcp = FastMCP("TimeMCP", 
              stateless_http=True) # no session persistence

@mcp.tool()
def time_now(timezone: str = "UTC") -> str:
    """
    Retourne l'heure actuelle dans le fuseau IANA donné (ex: 'Europe/Paris').
    """
    now = datetime.now(ZoneInfo(timezone))
    return now.isoformat()

@mcp.tool()
def convert_timezone(dt: str, from_tz: str, to_tz: str) -> str:
    """
    Convertit une datetime ISO d'un fuseau vers un autre.
    dt ex: '2025-09-05T14:00:00'
    """
    base = datetime.fromisoformat(dt)
    src = base.replace(tzinfo=ZoneInfo(from_tz))
    tgt = src.astimezone(ZoneInfo(to_tz))
    return tgt.isoformat()


if __name__ == "__main__":
    mcp.run(transport="streamable-http") 