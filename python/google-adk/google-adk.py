#!/usr/bin/env python3
"""
Google Agent Development Kit (ADK) Integration Example

This example demonstrates how to use the Xero MCP Server
with Google's Agent Development Kit to create AI agents that
can manage Xero accounting operations using MCP tools.
"""

import os
import asyncio
from typing import List, Dict, Any, Optional, Union
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types

# Load environment variables
load_dotenv()

# MCP Server Configuration
TS_MCP_SERVER_COMMAND = "@xeroapi/xero-mcp-server@latest"

def create_xero_mcp_toolset() -> MCPToolset:
    """Create the Xero MCP toolset for ADK integration."""
    return MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=[TS_MCP_SERVER_COMMAND],
            env_vars={
                "XERO_CLIENT_ID": os.getenv("XERO_CLIENT_ID"),
                "XERO_CLIENT_SECRET": os.getenv("XERO_CLIENT_SECRET"),
            },
        ),
        # Include comprehensive tool set for all demos
        tool_filter=[
            "list-contacts",
            "create-contact", 
            "list-invoices",
            "create-invoice",
            "get-timesheet",
            "list-accounts",
            "list-items",
            "list-tax-rates",
            "list-tracking-categories",
            "update-contact",
            "update-invoice",
            "create-payment",
            "list-payments",
            "list-organisation-details"
        ]
    )

# =============================================================================
# XeroADKAgent Class - Uses MCP Server for Xero operations
# =============================================================================

class XeroADKAgent:
    """
    Implementation of a Xero agent using Google ADK with Xero MCP Server.
    
    This demonstrates how to integrate Xero MCP tools with ADK's
    agent framework using the Xero MCP Server.
    """
    
    def __init__(self):
        """Initialize the ADK agent with Xero MCP tools."""
        self.agent = None
        self.runner = None
        self.session_service = None
        self.session = None
        self.xero_toolset = None
        
    async def initialize(self):
        """Initialize the agent and services asynchronously."""
        try:
            # Create the Xero MCP toolset and store reference for cleanup
            self.xero_toolset = create_xero_mcp_toolset()
            
            # Create the ADK agent with MCP tools
            self.agent = LlmAgent(
                name="xero_mcp_agent",
                model=os.getenv("DEFAULT_MODEL", "gemini-2.0-flash"),
                description="Xero Accounting Agent using MCP Server",
                instruction="""
                You are an intelligent Xero accounting agent with direct access to Xero's API through MCP tools.
                
                IMPORTANT: You must ONLY use the available MCP tools to interact with Xero. Do NOT generate code snippets or suggest alternative SDKs.
                
                Available MCP tools include:
                - list-contacts: List contacts/customers
                - create-contact: Create new contacts
                - list-invoices: List invoices
                - create-invoice: Create new invoices
                - list-accounts: List chart of accounts
                - list-organisation-details: Get organization information
                - list-payments: List payments
                - create-payment: Create payments
                
                When users ask for Xero operations:
                1. Use the appropriate MCP tool directly (e.g., call list-contacts for "show me contacts")
                2. Present the actual results from the tool call
                3. Explain what the data shows in user-friendly terms
                4. If you need to create something, use the create- tools
                
                Do NOT write Python code or reference other SDKs. Use the MCP tools exclusively.
                Always call the tools to get real data from the user's Xero account.
                """,
                tools=[self.xero_toolset],
            )
            
            # Create services
            self.session_service = InMemorySessionService()
            artifact_service = InMemoryArtifactService()
            memory_service = InMemoryMemoryService()
            
            # Create runner
            self.runner = Runner(
                app_name="xero_mcp_agent",
                agent=self.agent,
                session_service=self.session_service,
                artifact_service=artifact_service,
                memory_service=memory_service,
            )
            
            # Create session
            self.session = await self.session_service.create_session(
                state={}, 
                app_name="xero_mcp_agent", 
                user_id="demo_user"
            )
            
            print("✅ ADK agent initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize ADK agent: {e}")
            raise
    
    async def cleanup(self):
        """Clean up resources and close MCP connections."""
        try:
            if self.xero_toolset:
                # Try different cleanup methods for the MCP toolset
                cleanup_methods = [
                    ('close', lambda: self.xero_toolset.close()),
                    ('disconnect', lambda: self.xero_toolset.disconnect()),
                    ('cleanup', lambda: self.xero_toolset.cleanup()),
                    ('_client.close', lambda: self.xero_toolset._client.close() if hasattr(self.xero_toolset, '_client') else None),
                    ('_connection.close', lambda: self.xero_toolset._connection.close() if hasattr(self.xero_toolset, '_connection') else None)
                ]
                
                for method_name, method_call in cleanup_methods:
                    try:
                        if hasattr(self.xero_toolset, method_name.split('.')[0]):
                            result = method_call()
                            if result and hasattr(result, '__await__'):
                                await result
                            print(f"✅ Used {method_name} for cleanup")
                            break
                    except Exception as cleanup_error:
                        continue  # Try next method
                        
            # Force garbage collection to help with cleanup
            import gc
            gc.collect()
            print("✅ Agent cleanup completed")
        except Exception as e:
            print(f"⚠️ Warning during cleanup: {e}")
            # Even if cleanup fails, don't raise - just warn
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self.cleanup()
    
    async def process(self, query: str) -> str:
        """
        Process a user query using the ADK agent.
        """
        try:
            if not self.agent or not self.runner:
                await self.initialize()
                
            print(f"\n🤖 Processing: {query}")
            
            # Create content for the query
            content = types.Content(
                role='user', 
                parts=[types.Part(text=query)]
            )
            
            # Run the agent
            response_parts = []
            events_async = self.runner.run_async(
                session_id=self.session.id,
                user_id=self.session.user_id,
                new_message=content
            )
            
            async for event in events_async:
                try:
                    if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            # Handle text parts
                            if hasattr(part, 'text') and part.text:
                                response_parts.append(part.text)
                            # Handle function call parts (if any)
                            elif hasattr(part, 'function_call') and part.function_call is not None:
                                # Function calls are usually handled automatically by ADK
                                # but we can log them for debugging
                                if hasattr(part.function_call, 'name') and part.function_call.name:
                                    print(f"🔧 Function call: {part.function_call.name}")
                                else:
                                    print("🔧 Function call: [unnamed]")
                except Exception as part_error:
                    print(f"⚠️ Error processing response part: {part_error}")
                    continue
            
            result = ' '.join(response_parts) if response_parts else "I'm ready to help with Xero operations!"
            return result
            
        except Exception as e:
            error_msg = f"Error processing query '{query}': {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg


async def demo_basic_operations():
    """Demonstrate basic Xero operations with real ADK and MCP."""
    print("\n" + "="*50)
    print("BASIC XERO OPERATIONS WITH ADK + MCP SERVER")
    print("="*50)
    
    # Example queries
    queries = [
        "Show me a summary of my Xero account",
        "List my first 5 contacts",
        "Show me recent invoices"
    ]
    
    async with XeroADKAgent() as agent:
        for query in queries:
            print(f"\n📝 Query: {query}")
            try:
                result = await agent.process(query)
                print(f"✅ Result: {result}")
            except Exception as e:
                print(f"❌ Error processing '{query}': {e}")
                print(f"   Error type: {type(e).__name__}")
                # Try to get more details about the error
                import traceback
                print(f"   Traceback: {traceback.format_exc()}")
                
                # Continue with other queries
                continue


async def demo_invoice_workflow():
    """Demonstrate a complete invoice workflow with real ADK and MCP."""
    print("\n" + "="*50)
    print("INVOICE WORKFLOW WITH ADK + MCP SERVER")
    print("="*50)
    
    # Workflow steps
    workflow_queries = [
        "Create a new customer named 'Demo Company Inc' with email 'demo@company.com'",
        "List all customers to find the Demo Company",
        "Create an invoice for Demo Company Inc for 'ADK Integration Services' worth $750"
    ]
    
    async with XeroADKAgent() as agent:
        for i, query in enumerate(workflow_queries, 1):
            print(f"\n📌 Step {i}: {query}")
            try:
                result = await agent.process(query)
                print(f"✅ Result: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")


async def demo_natural_language_processing():
    """Demonstrate natural language understanding with real ADK and MCP."""
    print("\n" + "="*50)
    print("NATURAL LANGUAGE PROCESSING WITH ADK + MCP SERVER")
    print("="*50)
    
    # Natural language queries
    nl_queries = [
        "I need to bill my client $2,000 for consulting work",
        "Show me all my customers", 
        "What's the current state of my invoices?",
        "Create a new supplier called TechSupport Ltd with email support@techsupport.com"
    ]
    
    async with XeroADKAgent() as agent:
        for query in nl_queries:
            print(f"\n💬 Query: '{query}'")
            try:
                result = await agent.process(query)
                print(f"🤖 Agent: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")


async def demo_error_handling():
    """Demonstrate error handling in ADK + MCP integration."""
    print("\n" + "="*50)
    print("ERROR HANDLING IN ADK + MCP SERVER")
    print("="*50)
    
    # Test various scenarios that might cause errors
    error_scenarios = [
        "Create an invoice for a contact that doesn't exist with ID 'invalid-id'",
        "Get details for invoice with ID 'fake-invoice-123'",
        "List invoices with invalid status 'IMAGINARY'"
    ]
    
    async with XeroADKAgent() as agent:
        for scenario in error_scenarios:
            print(f"\n🧪 Testing: {scenario}")
            try:
                result = await agent.process(scenario)
                print(f"✅ Handled gracefully: {result}")
            except Exception as e:
                print(f"⚠️ Exception caught: {e}")


async def demo_batch_operations():
    """Demonstrate batch operations with real ADK and MCP."""
    print("\n" + "="*50)
    print("BATCH OPERATIONS WITH ADK + MCP SERVER")
    print("="*50)
    
    print("\nDemonstrating how ADK can handle multiple operations:")
    
    batch_query = """
    Please do the following operations in sequence:
    1. Get a summary of my Xero account
    2. List the first 3 contacts
    3. Show me any draft invoices
    Provide a summary of what you found.
    """
    
    async with XeroADKAgent() as agent:
        print(f"\n📋 Batch Query: {batch_query}")
        try:
            result = await agent.process(batch_query)
            print(f"✅ Batch Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")


async def interactive_demo():
    """Run an interactive demo with real ADK agent."""
    print("\n" + "="*50)
    print("INTERACTIVE ADK XERO AGENT")
    print("="*50)
    print("\nReal ADK agent with Xero MCP Server integration!")
    print("You can ask me to:")
    print("- List and create contacts")
    print("- List, create, and view invoices")
    print("- Get account summaries and organization details")
    print("- Manage payments and other accounting operations")
    print("\nType 'quit' to exit.\n")
    
    async with XeroADKAgent() as agent:
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n🤖 Agent: Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                result = await agent.process(user_input)
                print(f"\n🤖 Agent: {result}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


async def main():
    """Run the ADK integration examples."""
    # Check for required dependencies
    try:
        import google.adk
        print("✅ Google ADK is installed")
    except ImportError:
        print("❌ Google ADK is not installed. Please install with: pip install google-adk")
        return
    
    # Check for Xero credentials (MCP server only needs CLIENT_ID and CLIENT_SECRET)
    required_env_vars = ["XERO_CLIENT_ID", "XERO_CLIENT_SECRET"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables:")
        print("- XERO_CLIENT_ID: Your Xero app's client ID")
        print("- XERO_CLIENT_SECRET: Your Xero app's client secret")
        print("\nYou can get these from: https://developer.xero.com/")
        return
    
    # Check for model configuration
    if not os.getenv("DEFAULT_MODEL") and not os.getenv("GOOGLE_API_KEY") and not os.getenv("GOOGLE_GENAI_USE_VERTEXAI"):
        print("❌ Error: No model configuration found")
        print("Please set either:")
        print("- GOOGLE_API_KEY for Google AI Studio")
        print("- GOOGLE_GENAI_USE_VERTEXAI=TRUE for Vertex AI")
        return
    
    # Check for npx (required for MCP server)
    import shutil
    if not shutil.which("npx"):
        print("❌ Error: npx is not installed")
        print("Please install Node.js and npm to get npx")
        print("Visit: https://nodejs.org/")
        return
    
    print("Xero + Google ADK Integration Examples")
    print("======================================")
    print("Google ADK implementation with Xero MCP Server")
    print("Powered by Xero MCP Server tools\n")
    
    print("Select a demo:")
    print("1. Basic Operations") 
    print("2. Invoice Workflow")
    print("3. Natural Language Processing")
    print("4. Error Handling")
    print("5. Batch Operations")
    print("6. Interactive Demo")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    demos = {
        "1": demo_basic_operations,
        "2": demo_invoice_workflow, 
        "3": demo_natural_language_processing,
        "4": demo_error_handling,
        "5": demo_batch_operations,
        "6": interactive_demo
    }
    
    if choice in demos:
        try:
            await demos[choice]()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            print("Please check your environment configuration and try again.")
    else:
        print("Invalid choice. Please run again and select 1-6.")


if __name__ == "__main__":
    asyncio.run(main())