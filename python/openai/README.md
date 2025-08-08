# OpenAI Agents SDK + Xero MCP Integration

This project demonstrates how to use the OpenAI Agents SDK with the Xero MCP (Model Context Protocol) Server to create AI agents that can manage Xero accounting operations.

## Overview

The integration provides several specialized AI agents that can perform Xero accounting tasks:

- **General Xero Assistant**: A comprehensive agent with access to all Xero tools
- **Invoice Specialist**: Focused on invoice creation, management, and workflows
- **Contact Manager**: Specialized in customer and supplier contact management

## Features

- 🤖 **Multiple Agent Types**: Choose from specialized agents or a general-purpose assistant
- 📝 **Invoice Management**: Create, find, and manage invoices with natural language
- 👥 **Contact Operations**: Create and manage customers and suppliers
- 🔄 **Multi-Agent Workflows**: Demonstrate complex workflows using multiple specialized agents
- 💬 **Interactive Mode**: Chat directly with agents using natural language
- 🔍 **Comprehensive Examples**: Pre-built demos showing various use cases

## Prerequisites

### Required Software
- **Python 3.8+**
- **Node.js and npm/npx** (for the Xero MCP Server)

### Required API Keys
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
- **Xero Custom Connection Credentials**: 
  - Xero Client ID
  - Xero Client Secret
  - Get these by creating a custom connection Xero app at [Xero Developer Portal](https://developer.xero.com/)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js** (if not already installed):
   - Download from [nodejs.org](https://nodejs.org/)
   - The Xero MCP Server will be installed automatically via npx

3. **Set up environment variables:**
   Create a `.env` file in this directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   XERO_CLIENT_ID=your_xero_client_id_here
   XERO_CLIENT_SECRET=your_xero_client_secret_here
   ```

## Usage

### Running the Demo

Execute the main script to see the available demos:

```bash
python openai_agents.py
```

### Available Demos

1. **Basic Agent Demo**: Shows general Xero operations
2. **Invoice Specialist Demo**: Focused on invoice operations
3. **Contact Manager Demo**: Customer and supplier management
4. **Multi-Agent Workflow**: Demonstrates agent collaboration
5. **Comprehensive Workflow**: End-to-end process (Recommended)
6. **Interactive Agent**: Chat with agents in real-time

### Example Usage

#### Creating a Customer and Invoice

```python
# The agent can understand natural language requests:
"Create a new customer named 'Tech Solutions Inc' with email tech@solutions.com"

# Find customers to get contact IDs:
"Find customers with 'Tech' in their name and show me their contact IDs"

# Create an invoice using the contact ID:
"Create an invoice for contact ID 12345678-1234-1234-1234-123456789abc with line item: Consulting for $1000"
```

#### Working with Invoices

```python
# Find invoices by status:
"Find all draft invoices"
"Find all invoices with status AUTHORISED"

# Search by date:
"Find invoices from the last 30 days"
```

## Code Structure

### Agent Types

#### Basic Xero Agent
```python
agent = create_basic_xero_agent(mcp_server)
# Has access to all Xero tools and operations
```

#### Invoice Specialist
```python
agent = create_invoice_specialist_agent(mcp_server)
# Optimized for invoice creation and management
```

#### Contact Manager
```python
agent = create_contact_manager_agent(mcp_server)
# Specialized in customer and supplier operations
```

### Key Functions

- `create_basic_xero_agent()`: Creates a general-purpose Xero agent
- `create_invoice_specialist_agent()`: Creates an invoice-focused agent
- `create_contact_manager_agent()`: Creates a contact management agent
- `demo_*()` functions: Various demonstration scenarios
- `interactive_demo()`: Real-time chat interface

## Important Notes

### Contact IDs
- Xero uses UUID format for contact IDs (e.g., `12345678-1234-1234-1234-123456789abc`)
- Always find customers first to get valid contact IDs before creating invoices
- Contact IDs are required for invoice creation

### Best Practices
1. **Always verify contact IDs** before creating invoices
2. **Use natural language** - the agents understand conversational requests
3. **Start with contact creation** if you need new customers/suppliers
4. **Check agent responses** for confirmation of successful operations

## Error Handling

The script includes comprehensive error handling for:
- Missing environment variables
- Missing dependencies (openai-agents, npx)
- API connection issues
- Invalid user inputs

## Troubleshooting

### Common Issues

1. **"Please install openai-agents" error**:
   ```bash
   pip install openai-agents
   ```

2. **"npx is not installed" error**:
   - Install Node.js from [nodejs.org](https://nodejs.org/)
   - npx comes bundled with Node.js

3. **Environment variable errors**:
   - Ensure `.env` file exists with all required variables
   - Check that API keys are valid and active

4. **Xero authentication issues**:
   - Verify Xero app credentials are correct
   - Ensure your Xero app has proper permissions

## Example Workflows

### Complete Customer-to-Invoice Workflow

1. **Create Customer**:
   ```
   "Create a new customer named 'Demo Corp' with email billing@democorp.com"
   ```

2. **Find Customer ID**:
   ```
   "Find customers with 'Demo' in their name and show their contact IDs"
   ```

3. **Create Invoice**:
   ```
   "Create an invoice for contact ID [uuid-from-step-2] with line item: Consulting Services for $1500"
   ```

### Multi-Agent Coordination

```python
# Use Contact Manager to create customer
contact_agent = create_contact_manager_agent(mcp_server)
result = await Runner.run(contact_agent, "Create customer ABC Corp")

# Use Invoice Specialist to create invoice
invoice_agent = create_invoice_specialist_agent(mcp_server)
result = await Runner.run(invoice_agent, "Create invoice for ABC Corp")
```

## API Reference

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `XERO_CLIENT_ID` | Xero app client ID | Yes |
| `XERO_CLIENT_SECRET` | Xero app client secret | Yes |

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `openai-agents` | ≥0.1.0 | OpenAI Agents SDK |
| `python-dotenv` | ≥1.0.0 | Environment variable management |

## Contributing

To extend this integration:

1. Add new agent types by creating specialized agent functions
2. Implement additional demo scenarios in new `demo_*()` functions
3. Add error handling for specific Xero API scenarios
4. Create custom workflows for specific business processes

## License

This project is part of the Xero Agent Toolkit. Please refer to the main project license.

## Support

For issues related to:
- **OpenAI Agents SDK**: Check [OpenAI documentation](https://platform.openai.com/docs)
- **Xero API**: Visit [Xero Developer Portal](https://developer.xero.com/)
- **This Integration**: Create an issue in the main repository