#!/usr/bin/env python3
"""
OpenAI Agents SDK Integration Example

This example demonstrates how to use the Xero MCP Server
with the OpenAI Agents SDK to create AI agents that can
manage Xero accounting operations.
"""

import asyncio
import os
import shutil
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Note: You'll need to install openai-agents separately
# pip install openai-agents
try:
    from agents import Agent, Runner, gen_trace_id, trace
    from agents.mcp import MCPServer, MCPServerStdio
except ImportError:
    print("Please install openai-agents: pip install openai-agents")
    exit(1)


def create_basic_xero_agent(mcp_server: MCPServer) -> Agent:
    """
    Create a basic Xero agent with all tools.
    
    Args:
        mcp_server: The MCP server instance for Xero
    
    Returns:
        Configured Agent instance
    """
    agent = Agent(
        name="Xero Assistant",
        model="gpt-4o-mini",
        instructions="""You are a helpful accounting assistant that manages Xero operations. 
        You can create invoices, manage contacts, search for records, and handle various 
        accounting tasks. Always confirm successful operations and provide relevant details 
        to the user. Be precise with data handling and always verify important information.""",
        mcp_servers=[mcp_server]
    )
    
    return agent


def create_invoice_specialist_agent(mcp_server: MCPServer) -> Agent:
    """
    Create an agent that specializes in invoice operations.
    
    Args:
        mcp_server: The MCP server instance for Xero
    
    Returns:
        Configured Agent instance for invoice operations
    """
    agent = Agent(
        name="Invoice Specialist",
        model="gpt-4o-mini",
        instructions="""You are an invoice specialist for Xero. You excel at creating, 
        finding, and managing invoices. You understand accounting practices and can help 
        with invoice workflows. Always provide invoice numbers and IDs when creating or 
        finding invoices.""",
        mcp_servers=[mcp_server]
    )
    
    return agent


def create_contact_manager_agent(mcp_server: MCPServer) -> Agent:
    """
    Create an agent that specializes in contact management.
    
    Args:
        mcp_server: The MCP server instance for Xero
    
    Returns:
        Configured Agent instance for contact operations
    """
    agent = Agent(
        name="Contact Manager",
        model="gpt-4o-mini",
        instructions="""You are a contact management specialist for Xero. You help create, 
        find, and update customer and supplier information. You understand the importance 
        of accurate contact data for accounting and always validate important details.""",
        mcp_servers=[mcp_server]
    )
    
    return agent


async def demo_basic_agent(mcp_server: MCPServer):
    """Demonstrate the basic Xero agent capabilities."""
    print("\n" + "="*60)
    print("BASIC XERO AGENT DEMO")
    print("="*60)
    
    agent = create_basic_xero_agent(mcp_server)
    
    # Example requests
    requests = [
        "Find all active customers",
        "Create a new customer named 'Tech Solutions Inc' with email tech@solutions.com",
        "Find customers with 'Tech' in their name to see if our customer was created"
    ]
    
    for request in requests:
        print(f"\n🤖 User: {request}")
        print("💭 Agent thinking...")
        
        try:
            result = await Runner.run(starting_agent=agent, input=request)
            print(f"✅ Agent: {result.final_output}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n💡 Note: To create an invoice, you would need to:")
    print("    1. First get the contact_id from the customer creation response")
    print("    2. Then create an invoice using that specific contact_id")
    print("    3. Contact IDs in Xero are UUIDs, not simple strings like 'abc123'")


async def demo_invoice_specialist(mcp_server: MCPServer):
    """Demonstrate the invoice specialist agent."""
    print("\n" + "="*60)
    print("INVOICE SPECIALIST AGENT DEMO")
    print("="*60)
    
    agent = create_invoice_specialist_agent(mcp_server)
    
    # Example invoice-specific requests
    requests = [
        "Find all draft invoices",
        "Find all invoices with status AUTHORISED",
        "Find invoices from the last 30 days"
    ]
    
    for request in requests:
        print(f"\n📝 User: {request}")
        print("💭 Agent thinking...")
        
        try:
            result = await Runner.run(starting_agent=agent, input=request)
            print(f"✅ Agent: {result.final_output}")
        except Exception as e:
            print(f"❌ Error: {e}")


async def demo_contact_manager(mcp_server: MCPServer):
    """Demonstrate the contact manager agent."""
    print("\n" + "="*60)
    print("CONTACT MANAGER AGENT DEMO")
    print("="*60)
    
    agent = create_contact_manager_agent(mcp_server)
    
    # Example contact-specific requests
    requests = [
        "Find all customers",
        "Create a new supplier 'Office Supplies Ltd' with email orders@officesupplies.com",
        "Search for contacts with 'tech' in their name"
    ]
    
    for request in requests:
        print(f"\n👥 User: {request}")
        print("💭 Agent thinking...")
        
        try:
            result = await Runner.run(starting_agent=agent, input=request)
            print(f"✅ Agent: {result.final_output}")
        except Exception as e:
            print(f"❌ Error: {e}")


async def demo_multi_agent_workflow(mcp_server: MCPServer):
    """Demonstrate a workflow using multiple specialized agents."""
    print("\n" + "="*60)
    print("MULTI-AGENT WORKFLOW DEMO")
    print("="*60)
    
    contact_agent = create_contact_manager_agent(mcp_server)
    invoice_agent = create_invoice_specialist_agent(mcp_server)
    
    print("\n🔄 Step 1: Contact Manager creates a new customer")
    try:
        result1 = await Runner.run(
            starting_agent=contact_agent, 
            input="Create a new customer named 'Demo Corp' with email billing@democorp.com"
        )
        print(f"✅ Contact Agent: {result1.final_output}")
        
        print("\n🔄 Step 2: Find the customer we just created")
        result2 = await Runner.run(
            starting_agent=contact_agent,
            input="Find a customer named 'Demo Corp'"
        )
        print(f"✅ Contact Agent: {result2.final_output}")
        
        print("\n🔄 Step 3: Find existing customers to create an invoice for")
        result3 = await Runner.run(
            starting_agent=contact_agent,
            input="Find the first 3 customers"
        )
        print(f"✅ Contact Agent: {result3.final_output}")
        
        print("\n💡 Note: In a real application, you would extract the contact ID")
        print("    from the contact creation response and pass it to the invoice agent.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_comprehensive_workflow(mcp_server: MCPServer):
    """Demonstrate a comprehensive end-to-end workflow."""
    print("\n" + "="*60)
    print("COMPREHENSIVE WORKFLOW DEMO")
    print("="*60)
    print("This demo shows how to properly work with contact IDs and create invoices")
    
    # Create a general agent that has all tools
    agent = create_basic_xero_agent(mcp_server)
    
    print("\n🔄 Step 1: Create a new customer")
    try:
        result1 = await Runner.run(
            starting_agent=agent, 
            input="Create a new customer named 'Workflow Demo Ltd' with email demo@workflow.com"
        )
        print(f"✅ Agent: {result1.final_output}")
        
        print("\n🔄 Step 2: Find customers to get a valid contact ID")
        result2 = await Runner.run(
            starting_agent=agent,
            input="Find customers with 'Workflow' in their name and show me their contact IDs"
        )
        print(f"✅ Agent: {result2.final_output}")
        
        print("\n🔄 Step 3: Search for any existing customers we can use")
        result3 = await Runner.run(
            starting_agent=agent,
            input="Find the first 3 customers and show their contact IDs so I can create an invoice"
        )
        print(f"✅ Agent: {result3.final_output}")
        
        print("\n💡 Instructions for creating an invoice:")
        print("    1. Copy one of the contact IDs from above (the UUID format)")
        print("    2. Use that ID to create an invoice like this:")
        print("       'Create an invoice for contact ID [paste-uuid-here] with line item: Consulting for $1000'")
        print("    3. The contact ID must be in UUID format like: 12345678-1234-1234-1234-123456789abc")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def interactive_demo(mcp_server: MCPServer):
    """Run an interactive demo with the Agents SDK."""
    print("\n" + "="*60)
    print("INTERACTIVE XERO AGENTS SDK DEMO")
    print("="*60)
    print("\nChoose an agent type:")
    print("1. General Xero Assistant (all tools)")
    print("2. Invoice Specialist")
    print("3. Contact Manager")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        agent = create_basic_xero_agent(mcp_server)
        agent_name = "General Assistant"
    elif choice == "2":
        agent = create_invoice_specialist_agent(mcp_server)
        agent_name = "Invoice Specialist"
    elif choice == "3":
        agent = create_contact_manager_agent(mcp_server)
        agent_name = "Contact Manager"
    else:
        print("Invalid choice.")
        return
    
    print(f"\n🤖 {agent_name} is ready!")
    print("\nType your requests in natural language.")
    print("Examples:")
    print("- 'Create a new customer named ABC Corp with email info@abc.com'")
    print("- 'Find all customers'")
    print("- 'Find all draft invoices'")
    print("- 'Find customers and show their contact IDs'")
    print("\n⚠️  Important for creating invoices:")
    print("- Contact IDs must be in UUID format (e.g., 12345678-1234-1234-1234-123456789abc)")
    print("- Use 'Find customers' first to get valid contact IDs")
    print("- Then use: 'Create invoice for contact ID [uuid] with item: Description for $Amount'")
    print("\nType 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            print("💭 Agent thinking...")
            result = await Runner.run(starting_agent=agent, input=user_input)
            print(f"\n🤖 {agent_name}: {result.final_output}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def run_demo_with_mcp(mcp_server: MCPServer):
    """Run the selected demo with the MCP server."""
    print("Xero + OpenAI Agents SDK Integration Examples")
    print("=" * 50)
    
    print("\nSelect a demo:")
    print("1. Basic Agent Demo")
    print("2. Invoice Specialist Demo")
    print("3. Contact Manager Demo")
    print("4. Multi-Agent Workflow")
    print("5. Comprehensive Workflow (Recommended)")
    print("6. Interactive Agent")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        await demo_basic_agent(mcp_server)
    elif choice == "2":
        await demo_invoice_specialist(mcp_server)
    elif choice == "3":
        await demo_contact_manager(mcp_server)
    elif choice == "4":
        await demo_multi_agent_workflow(mcp_server)
    elif choice == "5":
        await demo_comprehensive_workflow(mcp_server)
    elif choice == "6":
        await interactive_demo(mcp_server)
    else:
        print("Invalid choice. Please run again and select 1-6.")


async def main():
    """Run the OpenAI Agents SDK integration examples."""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in environment")
        print("Please set your OpenAI API key to run this example")
        return
    
    if not os.getenv("XERO_CLIENT_ID") or not os.getenv("XERO_CLIENT_SECRET"):
        print("Error: Xero credentials not set in environment")
        print("Please set XERO_CLIENT_ID and XERO_CLIENT_SECRET")
        return
    
    # Check if npx is available
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    
    # Initialize MCP server and run demos
    async with MCPServerStdio(
        name="Xero",
        params={
            "command": "npx",
            "args": ["-y", "@xeroapi/xero-mcp-server@latest"],
            "env": {
                "XERO_CLIENT_ID": os.environ['XERO_CLIENT_ID'],
                "XERO_CLIENT_SECRET": os.environ['XERO_CLIENT_SECRET']
            }
        }
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Xero MCP Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            await run_demo_with_mcp(server)


if __name__ == "__main__":
    asyncio.run(main()) 