# Xero Google ADK Integration

This module demonstrates how to integrate Xero accounting operations with Google's Agent Development Kit (ADK) using the Xero MCP (Model Context Protocol) Server.

## Overview

The `google-adk.py` file provides a complete implementation of a Xero AI agent that can:

- List and create contacts/customers
- Manage invoices (list, create, view)
- Handle payments and accounting operations
- Process natural language queries about Xero data
- Demonstrate error handling and batch operations

## Features

- **Real-time Xero Integration**: Uses the Xero MCP Server for direct API access
- **Natural Language Processing**: Handles conversational queries about accounting data
- **Comprehensive Error Handling**: Graceful handling of API errors and edge cases
- **Interactive Demo Mode**: Run interactive sessions with the AI agent
- **Multiple Demo Scenarios**: Pre-built demos for different use cases

## Prerequisites

1. **Node.js and npm**: Required for the Xero MCP Server
   ```bash
   # Install Node.js from https://nodejs.org/
   node --version
   npm --version
   ```

2. **Xero Developer Account**: Get your credentials from [Xero Developer Portal](https://developer.xero.com/)
   - Client ID
   - Client Secret

3. **Google AI Configuration**: Set up either Google AI Studio or Vertex AI
   - For Google AI Studio: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - For Vertex AI: Set up Google Cloud project and authentication

## Installation

1. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```env
   # Xero API Credentials
   XERO_CLIENT_ID=your_xero_client_id
   XERO_CLIENT_SECRET=your_xero_client_secret
   
   # Google AI Configuration (choose one)
   # Option 1: Google AI Studio
   GOOGLE_API_KEY=your_google_ai_studio_api_key
   
   # Option 2: Vertex AI
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your_project_id
   
   # Optional: Specify model (defaults to gemini-2.0-flash)
   DEFAULT_MODEL=gemini-2.0-flash
   ```

## Usage

### Running the Interactive Demo

```bash
python google-adk.py
```

This will present you with several demo options:

1. **Basic Operations**: List contacts, invoices, and account summary
2. **Invoice Workflow**: Complete invoice creation workflow
3. **Natural Language Processing**: Process conversational queries
4. **Error Handling**: Demonstrate error scenarios
5. **Batch Operations**: Multiple operations in sequence
6. **Interactive Demo**: Chat-like interface with the agent

### Using as a Library

```python
import asyncio
from google-adk import XeroADKAgent

async def example():
    async with XeroADKAgent() as agent:
        # Ask natural language questions
        result = await agent.process("Show me my recent invoices")
        print(result)
        
        # Create new contacts
        result = await agent.process("Create a new customer named ABC Corp")
        print(result)

# Run the example
asyncio.run(example())
```

### Available MCP Tools

The agent has access to these Xero MCP tools:

- `list-contacts`: List all contacts/customers
- `create-contact`: Create new contacts
- `list-invoices`: List invoices with filtering
- `create-invoice`: Create new invoices
- `list-accounts`: List chart of accounts
- `list-items`: List inventory items
- `list-tax-rates`: List available tax rates
- `list-tracking-categories`: List tracking categories
- `update-contact`: Update existing contacts
- `update-invoice`: Update draft invoices
- `create-payment`: Create payments against invoices
- `list-payments`: List existing payments
- `list-organisation-details`: Get organization information

## Example Queries

The agent can handle natural language queries like:

- "Show me a summary of my Xero account"
- "List my first 5 contacts"
- "Create a new customer named Demo Company Inc with email demo@company.com"
- "Create an invoice for Demo Company Inc for consulting services worth $750"
- "What's the current state of my invoices?"
- "Show me all my customers"
- "I need to bill my client $2,000 for consulting work"

## Architecture

The integration uses:

- **Google ADK**: For AI agent framework and natural language processing
- **Xero MCP Server**: For secure, structured access to Xero API
- **Model Context Protocol**: For tool communication between ADK and Xero
- **Async/Await**: For non-blocking operations and better performance

## Error Handling

The agent includes comprehensive error handling for:

- Missing environment variables
- Network connectivity issues
- Invalid Xero API responses
- Tool execution failures
- Async operation cleanup

## Troubleshooting

### Common Issues

1. **"npx is not installed"**
   - Install Node.js from https://nodejs.org/

2. **"Missing required environment variables"**
   - Check your `.env` file has all required Xero credentials

3. **"Google ADK is not installed"**
   - Run `pip install -r requirements.txt`

4. **"No model configuration found"**
   - Set either `GOOGLE_API_KEY` or `GOOGLE_GENAI_USE_VERTEXAI=TRUE`

### Debug Mode

Enable debug output by setting:
```env
GOOGLE_GENAI_LOG_LEVEL=DEBUG
```

## Contributing

When extending this integration:

1. Add new MCP tools to the `tool_filter` in `create_xero_mcp_toolset()`
2. Update the agent instructions to include new capabilities
3. Add corresponding demo scenarios
4. Update this README with new features