
import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("support-tools")
DB_PATH = "support_copilot/data/support.db"

@mcp.tool()
def get_customer_info(name: str):
    """
    Get customer information from SQL database.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE name LIKE ?",
        (f"%{name}%",)
    )

    result = cursor.fetchall()
    conn.close()

    if not result:
        return "Customer not found"

    return str(result)

@mcp.tool()
def search_policy(query: str):
    """
    Search company policy documents.
    """
    # Later connect Chroma vector search here
    return f"Searching policy documents for: {query}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
