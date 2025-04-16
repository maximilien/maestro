import os, json

from mcp.server.fastmcp import FastMCP

# MCP globals
mcp = FastMCP("a simple MCP server")

@mcp.tool()
async def echo_tool(message: str) -> str:
    """A simple echo tool to that echoes back message sent
        Args:
            message: a message to echo back
    """    
    return message

@mcp.tool()
async def test_tool() -> str:
    """A simple test tool to check connections
    """    
    return "all you need is attention!"

if __name__ == "__main__":
    print(f"Connected to MCP server https://{mcp.settings.host}:{mcp.settings.port}")
    mcp.run(transport='stdio')

# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()


# @app.get("/healthcheck/")
# def healthcheck():
#     return 'Health - OK'

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=30000)