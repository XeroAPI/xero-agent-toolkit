# Xero Agent Toolkit

A comprehensive collection of examples demonstrating how to build AI agents that integrate with the Xero API using various agentic frameworks and the Xero MCP (Model Context Protocol) Server.

## Overview

This repository provides practical examples of building intelligent agents that can interact with Xero accounting data using different AI frameworks. Each example demonstrates how to leverage the [Xero MCP Server](https://github.com/xeroapi/xero-mcp-server) to provide agents with structured access to Xero's comprehensive accounting functionality.

### What You Can Build

The examples in this repository show how to create AI agents that can:

- 📝 **Manage Invoices**: Create, update, and track invoices with natural language
- 👥 **Handle Contacts**: Create and manage customers and suppliers
- 💰 **Process Payments**: Record and track payments against invoices
- 👨‍💼 **Payroll Operations**: Manage employees, timesheets, and leave (where applicable)
- 💬 **Natural Language Interface**: Process conversational queries about accounting data

## Available Examples

### Python Implementations

#### 🔗 [Google ADK Integration](./python/google-adk/)
Demonstrates integration with Google's Agent Development Kit (ADK), featuring:
- Real-time Xero integration via MCP
- Natural language processing for accounting queries
- Interactive demo modes and batch operations
- Comprehensive error handling

#### 🦜 [LangChain Integration](./python/langchain/)
Advanced LangChain integration showcasing:
- Specialized agents (Invoice Specialist, Contact Manager)
- Multi-step business workflows
- Intelligent invoice analysis and recommendations
- Async/await support for optimal performance

#### 🤖 [OpenAI Agents SDK](./python/openai/)
OpenAI Agents SDK implementation featuring:
- Multiple specialized agent types
- Multi-agent collaboration workflows
- Interactive chat interfaces
- Comprehensive example scenarios

### TypeScript Implementations

#### 🔧 [OpenAI Agents SDK (TypeScript)](./typescript/openai-agents/)
TypeScript implementation of OpenAI Agents SDK with:
- Type-safe Xero operations
- Modern async/await patterns
- Interactive demo modes
- Comprehensive agent workflows

#### 🦜 [LangChain (TypeScript)](./typescript/langchain/)
TypeScript LangChain integration featuring:
- Specialized agents (Invoice Specialist, Contact Manager)
- Multi-step business workflows and invoice analysis
- Interactive chat interface with real-time Xero operations
- Organization insights and comprehensive reporting
- Type-safe operations with @langchain/mcp-adapters

## Prerequisites

### Required for All Examples
- **Xero Developer Account**: Get your credentials from [Xero Developer Portal](https://developer.xero.com/)
  - Client ID
  - Client Secret
Make sure you are create a [Custom Connection](https://developer.xero.com/documentation/guides/oauth2/custom-connections) type of app - Web app and PKCE apps will not work with these examples
- **Node.js and npm**: Required for the Xero MCP Server

### Framework-Specific Requirements
- **Google ADK**: Google AI Studio API key or Vertex AI setup
- **LangChain**: OpenAI API key
- **OpenAI Agents**: OpenAI API key

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xeroapi/xero-agent-toolkit.git
   cd xero-agent-toolkit
   ```

2. **Choose your preferred framework** and navigate to its directory

3. **Follow the specific README** in each subdirectory for detailed setup instructions

4. **Set up your environment variables** as specified in each example

5. **Run the examples** to see AI agents in action with Xero

## Architecture

All examples in this repository use the **Xero MCP Server** as the bridge between AI frameworks and the Xero API. This architecture provides:

- **Standardized Interface**: Consistent tool definitions across all frameworks
- **Secure Authentication**: OAuth2 flow handled by the MCP server
- **Type Safety**: Structured schemas for all Xero operations
- **Error Handling**: Robust error management and retry logic

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Framework  │ ←→ │  Xero MCP       │ ←→ │   Xero API      │
│  (LangChain,    │    │  Server         │    │                 │
│   OpenAI, etc.) │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Example Use Cases

### Business Automation
- Automated monthly invoicing workflows
- Customer onboarding with contact creation
- Payment processing and reconciliation
- Financial reporting and analysis

### Conversational Accounting
- "Create an invoice for ABC Corp for $1,500 consulting services"
- "Show me all overdue invoices"
- "What's my profit and loss for this quarter?"
- "Create a new customer named XYZ Ltd with email contact@xyz.com"

### Multi-Agent Workflows
- Contact Manager → Invoice Specialist collaboration
- Automated end-to-end business processes
- Intelligent data analysis and recommendations

## Getting Help

- **Framework-specific issues**: Check the README in each subdirectory
- **Xero API questions**: Visit [Xero Developer Portal](https://developer.xero.com/)
- **MCP Server issues**: See [Xero MCP Server repository](https://github.com/xeroapi/xero-mcp-server)
- **General questions**: Open an issue in this repository

## Contributing

We welcome contributions! Whether you want to:
- Add support for new AI frameworks
- Improve existing examples
- Add new use cases or workflows
- Fix bugs or improve documentation

Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Related Projects

- [Xero MCP Server](https://github.com/xeroapi/xero-mcp-server) - The Model Context Protocol server for Xero
- [Model Context Protocol](https://modelcontextprotocol.io/) - The open standard for connecting AI systems
- [Xero API Documentation](https://developer.xero.com/documentation/) - Official Xero API docs

---

**Ready to build intelligent accounting agents?** Choose your preferred framework from the examples above and start building! 🚀