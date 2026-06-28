from mcp.server.fastmcp import FastMCP

mcp = FastMCP("travel-tools")

@mcp.tool()
def get_travel_tip(city: str) -> str:
    """Return a simple travel tip for a city."""
    if city.lower() == "naples":
        return "Naples is a good base for Pompeii, Vesuvius, and the Amalfi Coast."

    if city.lower() == "paris":
        return "Paris is a good city for museums, walking neighborhoods, and day trips by train."

    return f"No travel tip is available for {city}."


if __name__ == "__main__":

    mcp.run()
