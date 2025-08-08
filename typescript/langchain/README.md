# LangChain + Xero MCP Integration (TypeScript)

This project demonstrates how to integrate LangChain with the Xero MCP (Model Context Protocol) Server to create AI agents that can manage Xero accounting operations using natural language.

## Overview

This TypeScript implementation showcases advanced LangChain patterns with the Xero MCP server, including specialized agents, complex workflows, and various integration patterns using the `@langchain/mcp-adapters` library.

## Features

- 🤖 **Specialized Agent Demos**: Different agents for invoicing, contacts, and general operations
- 📝 **Invoice Management**: Create, find, and analyze invoices with AI assistance
- 👥 **Contact Operations**: Manage customers and suppliers using natural language
- 🔄 **Multi-Step Workflows**: Complex business process automation
- 📊 **Organization Insights**: Get AI-powered analysis of your Xero data
- 💬 **Interactive Mode**: Real-time chat with your Xero AI assistant
- 🔧 **LangGraph Integration**: Uses the latest LangGraph prebuilt agents

## Prerequisites

### Required Software
- **Node.js** (version 18 or higher)
- **npm** or **yarn**

### Required API Keys
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
- **Xero Custom Connection Credentials**: 
  - Xero Client ID
  - Xero Client Secret
  - Get these by creating a custom connection Xero app at [Xero Developer Portal](https://developer.xero.com/)

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env` file in this directory with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   XERO_CLIENT_ID=your_xero_client_id_here
   XERO_CLIENT_SECRET=your_xero_client_secret_here
   ```

   **Important:** You must have valid Xero API credentials and an active OpenAI API key for the application to work properly.

## Running the Application

To start the application:
```bash
npm start
# or
npx ts-node index.ts
```

## Available Demos

The application includes six interactive demo modes:

1. **Invoice Specialist Agent** - Focused on invoice creation and management
2. **Contact Manager Agent** - Customer and supplier management
3. **Multi-Step Workflow** - Monthly invoicing process automation
4. **Invoice Analysis** - AI-powered invoice insights and recommendations
5. **Interactive Xero Agent** - Real-time chat interface
6. **Organization Insights** - Comprehensive Xero account analysis

## Agent Capabilities

### Invoice Specialist Agent
- Find and manage draft invoices
- Create invoices for customers
- Calculate billing amounts and line items
- Track invoice statuses and workflows

### Contact Manager Agent
- Create new customers and suppliers
- Search and find existing contacts
- Manage contact information and details
- Validate contact data for accuracy

### Multi-Step Workflow Agent
- Execute complex business processes
- Coordinate multiple Xero operations
- Provide step-by-step guidance
- Automate routine monthly tasks

### Organization Insights Agent
- Analyze Xero organization data
- Provide business recommendations
- Generate reports and summaries
- Track key performance indicators

## Example Operations

### Creating a Customer and Invoice
```typescript
// Natural language examples the agent can understand:
"Create a new customer called 'Demo Corp' with email demo@demo.com"
"Find all active customers"
"Create an invoice for Demo Corp for 10 hours of consulting at $150 per hour"
```

### Invoice Management
```typescript
"Find all draft invoices"
"Show me recent invoices that are overdue"
"Analyze invoice payment patterns"
```

### Organization Analysis
```typescript
"Get organization details and provide insights"
"Summarize my contact database"
"Analyze recent invoice trends"
```

## Technical Implementation

### LangChain Integration
- Uses `@langchain/mcp-adapters` for seamless MCP integration
- Leverages `createReactAgent` from LangGraph for intelligent decision-making
- Implements GPT-4o for enhanced reasoning capabilities
- Automatic tool discovery and wrapping

### Key Components
```typescript
// Agent creation with MCP integration
const client = new MultiServerMCPClient({
    xero: {
        transport: 'stdio',
        command: 'npx',
        args: ['-y', '@xeroapi/xero-mcp-server@latest'],
        env: { XERO_CLIENT_ID, XERO_CLIENT_SECRET }
    }
});

const tools = await client.getTools();
const agent = createReactAgent({ llm, tools });
```

## Important Notes

### Contact IDs
- Xero uses UUID format for contact IDs (e.g., `12345678-1234-1234-1234-123456789abc`)
- Always find customers first to get valid contact IDs before creating invoices
- The agents will automatically handle contact ID management

### Best Practices
1. **Start with contact creation** if you need new customers/suppliers
2. **Use natural language** - the agents understand conversational requests
3. **Review agent responses** for confirmation of successful operations
4. **Leverage multi-step workflows** for complex business processes

## Error Handling

The application includes comprehensive error handling for:
- Missing environment variables
- Invalid API credentials
- Network connectivity issues
- Xero API rate limits
- Invalid user inputs

## Troubleshooting

### Common Issues

1. **Environment variable errors**:
   - Ensure `.env` file exists with all required variables
   - Check that API keys are valid and active

2. **Xero authentication issues**:
   - Verify Xero app credentials are correct
   - Ensure your Xero app has proper permissions

3. **Node.js version issues**:
   - Use Node.js 18 or higher
   - Update npm to the latest version

4. **MCP Server connection issues**:
   - Ensure npx is available (comes with Node.js)
   - Check internet connectivity for downloading the MCP server

## Development

### Development Scripts
```bash
# Start with development mode
npm start

# Build TypeScript
npm run build

# Type checking
npx tsc --noEmit
```

### Project Structure
```
typescript/langchain/
├── index.ts          # Main application file
├── package.json      # Dependencies and scripts
├── tsconfig.json     # TypeScript configuration
└── README.md         # This file
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
| `@langchain/core` | ^0.3.67 | Core LangChain functionality |
| `@langchain/langgraph` | ^0.4.3 | Agent creation and workflows |
| `@langchain/openai` | ^0.6.4 | OpenAI model integration |
| `@langchain/mcp-adapters` | ^0.6.0 | MCP protocol adapters |
| `dotenv` | ^16.4.5 | Environment variable management |

## Contributing

To extend this integration:

1. Add new specialized agents in the main file
2. Implement additional demo scenarios with new functions
3. Create custom workflows for specific business processes
4. Add error handling for specific Xero API scenarios

## License

This project is part of the Xero Agent Toolkit. Please refer to the main project license.

## Support

For issues related to:
- **LangChain**: Check [LangChain documentation](https://docs.langchain.com/)
- **OpenAI API**: Visit [OpenAI documentation](https://platform.openai.com/docs)
- **Xero API**: Visit [Xero Developer Portal](https://developer.xero.com/)
- **This Integration**: Create an issue in the main repository