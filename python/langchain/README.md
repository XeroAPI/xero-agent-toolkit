# LangChain Xero Integration

This project demonstrates advanced integration between LangChain and the Xero MCP (Model Context Protocol) Server, providing a powerful framework for building AI agents that can interact with Xero accounting data.

## Overview

The `langchain.py` file contains several specialized agents and workflows that showcase different use cases for integrating LangChain with Xero through the MCP protocol. This integration allows you to build intelligent agents that can perform complex accounting operations, analyze financial data, and automate business processes.

## Features

### 🤖 Specialized Agents
- **Invoice Specialist Agent**: Focuses on invoice operations, creation, and management
- **Contact Manager Agent**: Handles customer and supplier contact management
- **Interactive Chat Agent**: Provides a conversational interface for Xero operations

### 📊 Advanced Workflows
- **Multi-step Workflows**: Complex business processes like monthly invoicing
- **Invoice Analysis**: Intelligent analysis of invoice data with recommendations
- **Organization Insights**: Comprehensive business intelligence and reporting

### 🔧 Technical Features
- Automatic tool discovery and integration via MCP
- Async/await support for optimal performance
- Error handling and robust exception management
- Environment-based configuration

## Prerequisites

### Environment Variables
Create a `.env` file in the project directory with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Xero API Configuration
XERO_CLIENT_ID=your_xero_client_id
XERO_CLIENT_SECRET=your_xero_client_secret
```

### Xero Setup
1. Create a Xero Developer Account at [developer.xero.com](https://developer.xero.com)
2. Create a new app and obtain your Client ID and Client Secret
3. Configure the appropriate scopes for your use case

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install the Xero MCP Server:**
   ```bash
   npm install -g @xeroapi/xero-mcp-server@latest
   ```

3. **Set up environment variables:**
   Create a `.env` file with your API keys (see Prerequisites section)

## Usage

### Running the Demo

Execute the main script to access the interactive demo menu:

```bash
python langchain.py
```

You'll be presented with the following options:

1. **Invoice Specialist Agent** - Demonstrates invoice-focused operations
2. **Contact Manager Agent** - Shows contact management capabilities
3. **Multi-step Workflow** - Complex business process automation
4. **Invoice Analysis** - Intelligent financial data analysis
5. **Interactive Chat** - Conversational interface with your Xero data
6. **Organization Insights** - Business intelligence and reporting

### Code Examples

#### Creating a Basic Xero Agent

```python
from langchain.py import create_xero_mcp_agent
from langchain_core.messages import HumanMessage

async def example_usage():
    # Create the agent
    agent, client = await create_xero_mcp_agent()
    
    # Use the agent
    response = await agent.ainvoke({
        "messages": [HumanMessage(content="Find all draft invoices")]
    })
    
    # Process the response
    if response and "messages" in response:
        result = response["messages"][-1].content
        print(f"Agent response: {result}")
```

#### Custom Workflow Example

```python
async def custom_workflow():
    agent, client = await create_xero_mcp_agent()
    
    workflow_steps = [
        "List all customers",
        "Find overdue invoices",
        "Calculate total outstanding amount"
    ]
    
    for step in workflow_steps:
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=step)]
        })
        # Process each step...
```

## Architecture

### MCP Integration
The project uses the `langchain-mcp-adapters` library to seamlessly integrate with the Xero MCP Server. This provides:

- **Automatic Tool Discovery**: Tools are automatically discovered from the MCP server
- **Type Safety**: Proper typing and validation for all Xero API operations
- **Error Handling**: Robust error handling and retry mechanisms

### Agent Architecture
The agents are built using LangGraph's `create_react_agent` pattern, providing:

- **ReAct Framework**: Reasoning and Acting capabilities
- **Tool Integration**: Seamless integration with Xero MCP tools
- **Context Management**: Proper conversation context and memory

## Available Xero Operations

The integration provides access to comprehensive Xero functionality including:

### Contacts
- Create, update, and search contacts
- Manage customer and supplier information
- Contact group management

### Invoices
- Create and update invoices
- Process payments
- Invoice analysis and reporting

### Financial Reports
- Profit & Loss statements
- Balance sheets
- Trial balance
- Aged receivables/payables

### Banking
- Bank transaction management
- Reconciliation support

### Payroll (if enabled)
- Employee management
- Timesheet processing
- Leave management

## Error Handling

The project includes comprehensive error handling:

```python
try:
    response = await agent.ainvoke({"messages": [HumanMessage(content=query)]})
    # Process response...
except Exception as e:
    print(f"❌ Error: {e}")
    # Handle error appropriately...
```

## Development

### Project Structure
```
python/langchain/
├── langchain.py          # Main integration file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Extending the Integration

To add new functionality:

1. **Create Custom Agents**: Follow the pattern in existing demo functions
2. **Add New Workflows**: Implement multi-step business processes
3. **Custom Tools**: Extend with additional MCP tools if needed

### Testing

Before running the integration:

1. Ensure all environment variables are set
2. Verify Xero API credentials are valid
3. Test with a Xero sandbox environment first

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   ```
   Error: OPENAI_API_KEY not set in environment
   ```
   Solution: Create a `.env` file with all required variables

2. **Xero Authentication Errors**
   ```
   Error: Xero credentials not set in environment
   ```
   Solution: Verify your Xero Client ID and Secret are correct

3. **MCP Server Connection Issues**
   ```
   Error connecting to MCP server
   ```
   Solution: Ensure the Xero MCP server is installed: `npm install -g @xeroapi/xero-mcp-server@latest`

### Debug Mode

For additional debugging information, set the environment variable:
```bash
export DEBUG=1
```

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Xero Agent Toolkit. Please refer to the main repository for licensing information.

## Support

For support and questions:

1. Check the [Xero Developer Documentation](https://developer.xero.com)
2. Review the [LangChain Documentation](https://python.langchain.com)
3. Open an issue in the main repository

## Related Projects

- [Xero MCP Server](https://github.com/xeroapi/xero-mcp-server)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)