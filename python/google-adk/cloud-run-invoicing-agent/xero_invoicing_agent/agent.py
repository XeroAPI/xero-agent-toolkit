import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

BASEDIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASEDIR, "../.env"))

TS_MCP_SERVER_COMMAND = "@xeroapi/xero-mcp-server@latest"

my_env_vars = {
    "XERO_CLIENT_ID": os.getenv("XERO_CLIENT_ID"),
    "XERO_CLIENT_SECRET": os.getenv("XERO_CLIENT_SECRET"),
}

xero_mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[TS_MCP_SERVER_COMMAND],
        env_vars=my_env_vars,
    ),
    tool_filter=[
        "list-contacts",
        "list-items",
        "list-tax-rates",
        "list-accounts",
        "list-tracking-categories",
        "create-invoice",
        "list-invoices",
        "update-invoice",
    ]
)

root_agent = Agent(
    name="xero_invoicing_agent",
    model=os.getenv("DEFAULT_MODEL"),
    description="Xero Invoicing Agent",
    instruction="""
    You are an invoicing agent that can create invoices for Xero.
    You will be given a description of the invoice and a list of items to be invoiced.
    You will need to create an invoice for the items and send it to the customer.
    You will need to use the list_contacts tool to get the customer details.
    You will need to use the list_items tool to get the item details.
    You will need to use the list_tax_rates tool to get the tax details.
    You will need to use the create_invoice tool to create the invoice.
    """,
    tools=[xero_mcp_toolset],
)