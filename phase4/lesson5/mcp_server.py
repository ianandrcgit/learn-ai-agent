from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("My AI Tools Server")


# --- TOOL 1: Calculator ---
@mcp.tool()
def calculate(expression: str) -> str:
    """Calculate a mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


# --- TOOL 2: Word Counter ---
@mcp.tool()
def count_words(text: str) -> str:
    """Count the number of words in a text"""
    count = len(text.split())
    return f"Word count: {count}"


# --- TOOL 3: Text Reverser ---
@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a piece of text"""
    return f"Reversed: {text[::-1]}"


if __name__ == "__main__":
    print("Starting MCP Server...")
    mcp.run()