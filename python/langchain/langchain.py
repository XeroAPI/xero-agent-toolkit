#!/usr/bin/env python3
"""
Advanced LangChain Integration with Xero MCP Server

This example demonstrates advanced use cases for the Xero MCP server
with LangChain, including specialized agents, complex workflows,
and various integration patterns using the langchain-mcp-adapters library.
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Standard LangChain imports
try:
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent
    from langchain_core.messages import HumanMessage
except ImportError:
    print("Please install langchain: pip install langchain langchain-openai langgraph")
    exit(1)

# Standard MCP adapter imports
try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
except ImportError:
    print("Please install MCP adapters: pip install langchain-mcp-adapters")
    exit(1)


async def create_xero_mcp_agent():
    """
    Create a LangChain agent using the Xero MCP Server.
    """
    
    # Configure the MCP client
    client = MultiServerMCPClient({
        "xero": {
            "transport": "stdio",  # or "sse" for HTTP transport
            "command": "npx",
            "args": ["-y", "@xeroapi/xero-mcp-server@latest"],
            "env": {
                "XERO_CLIENT_ID": os.getenv("XERO_CLIENT_ID"),
                "XERO_CLIENT_SECRET": os.getenv("XERO_CLIENT_SECRET"),
            }
        }
    })
    
    # Get tools automatically - no manual tool wrapping needed!
    tools = await client.get_tools()
    
    # Create LLM - using GPT-4o for larger context window
    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    
    # Create agent using the standard LangGraph approach
    agent = create_react_agent(llm, tools)
    
    return agent, client


async def demo_invoice_specialist_agent():
    """Demonstrate an agent that specializes in invoice operations."""
    print("\n" + "="*50)
    print("INVOICE SPECIALIST AGENT")
    print("="*50)
    
    agent, client = await create_xero_mcp_agent()
    
    # Example queries - more focused and realistic
    queries = [
        "Find all draft invoices",
        "Find the first 3 customers",
        "Create an invoice for one of the customers found for 10 hours of consulting at $150 per hour"
    ]
    
    try:
        for query in queries:
            print(f"\n📝 Query: {query}")
            
            # Use the agent - standard LangGraph invocation
            response = await agent.ainvoke({
                "messages": [HumanMessage(content=query)]
            })
            
            # Extract the response content
            if response and "messages" in response:
                last_message = response["messages"][-1]
                print(f"\n✅ Response: {last_message.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def demo_contact_manager_agent():
    """Demonstrate an agent that manages contacts."""
    print("\n" + "="*50)
    print("CONTACT MANAGER AGENT")
    print("="*50)
    
    agent, client = await create_xero_mcp_agent()
    
    # Example queries
    queries = [
        "Create a new customer called 'Demo Corp' with email demo@demo.com",
        "Find all suppliers",
        "Search for contacts with 'demo' in their name"
    ]
    
    try:
        for query in queries:
            print(f"\n📝 Query: {query}")
            
            # Use the agent - standard LangGraph invocation
            response = await agent.ainvoke({
                "messages": [HumanMessage(content=query)]
            })
            
            # Extract the response content
            if response and "messages" in response:
                last_message = response["messages"][-1]
                print(f"\n✅ Response: {last_message.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def demo_multi_step_workflow():
    """Demonstrate a multi-step workflow."""
    print("\n" + "="*50)
    print("MULTI-STEP WORKFLOW: MONTHLY INVOICING")
    print("="*50)
    
    agent, client = await create_xero_mcp_agent()
    
    workflow_prompt = """
    Please help me with monthly invoicing:
    1. First, find all active customers
    2. Show me the first 3 customers found
    3. Explain how I could create invoices for them (but don't actually create them yet)
    """
    
    print(f"\n📋 Workflow Request: {workflow_prompt}")
    
    try:
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=workflow_prompt)]
        })
        
        if response and "messages" in response:
            last_message = response["messages"][-1]
            print(f"\n✅ Workflow Result: {last_message.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def demo_invoice_analysis():
    """Demonstrate invoice analysis."""
    print("\n" + "="*50)
    print("INVOICE ANALYSIS")
    print("="*50)
    
    agent, client = await create_xero_mcp_agent()
    
    analysis_prompt = """
    Please help me analyze my invoices:
    1. Find a recent invoice
    2. Provide analysis including total amount, payment status, and any recommendations
    3. If overdue, calculate days overdue
    """
    
    print(f"\n📊 Analysis Request: {analysis_prompt}")
    
    try:
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=analysis_prompt)]
        })
        
        if response and "messages" in response:
            last_message = response["messages"][-1]
            print(f"\n✅ Analysis Result: {last_message.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def interactive_mcp_demo():
    """Run an interactive demo with the example agent."""
    print("\n" + "="*50)
    print("INTERACTIVE XERO AGENT")
    print("="*50)
    print("\nChat with your Xero agent. The agent has access to all Xero functions.")
    print("Type 'quit' to exit.\n")
    
    agent, client = await create_xero_mcp_agent()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n🤖 Assistant: Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = await agent.ainvoke({
                "messages": [HumanMessage(content=user_input)]
            })
            
            if response and "messages" in response:
                last_message = response["messages"][-1]
                print(f"\n🤖 Assistant: {last_message.content}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def demo_organization_insights():
    """Demonstrate getting organization insights."""
    print("\n" + "="*50)
    print("ORGANIZATION INSIGHTS")
    print("="*50)
    
    agent, client = await create_xero_mcp_agent()
    
    insights_prompt = """
    Please provide me with insights about my Xero organization:
    1. Get the organization details
    2. Get a summary of contacts (total count, types)
    3. Get a summary of recent invoices
    4. Provide any recommendations for better organization
    """
    
    print(f"\n📈 Insights Request: {insights_prompt}")
    
    try:
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=insights_prompt)]
        })
        
        if response and "messages" in response:
            last_message = response["messages"][-1]
            print(f"\n✅ Insights: {last_message.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")



def main():
    """Run the MCP integration examples."""
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in environment")
        return
    
    if not os.getenv("XERO_CLIENT_ID") or not os.getenv("XERO_CLIENT_SECRET"):
        print("Error: Xero credentials not set in environment")
        print("Please set XERO_CLIENT_ID and XERO_CLIENT_SECRET")
        return
    
    print("LangChain + Xero MCP Integration Examples")
    print("========================================\n")
    
    print("Select a demo:")
    print("1. Invoice Specialist Agent")
    print("2. Contact Manager Agent")
    print("3. Multi-step Workflow")
    print("4. Invoice Analysis")
    print("5. Interactive Chat")
    print("6. Organization Insights")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    demos = {
        "1": demo_invoice_specialist_agent,
        "2": demo_contact_manager_agent,
        "3": demo_multi_step_workflow,
        "4": demo_invoice_analysis,
        "5": interactive_mcp_demo,
        "6": demo_organization_insights
    }
    
    if choice in demos:
        asyncio.run(demos[choice]())
    else:
        print("Invalid choice. Please run again and select 1-6.")


if __name__ == "__main__":
    main()