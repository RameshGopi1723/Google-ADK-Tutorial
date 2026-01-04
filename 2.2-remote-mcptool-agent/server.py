from mcp.server.fastmcp import FastMCP
import requests

# create server
mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(city: str) -> str:
    """Fetch weather data for a given city."""
    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text
    

if __name__ == "__main__":
    # running with sse transport
    # mcp.run(transport="sse")
    
    # running with streamable-http transport
    mcp.run(transport="streamable-http")