# Xero OpenAI Agents SDK Integration

This project demonstrates how to use the OpenAI Agents SDK with the Xero MCP Server to create AI agents that can manage Xero accounting operations.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn
- OpenAI API key
- Xero API credentials (Client ID and Client Secret)

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Copy the `.env.template` file to `.env` and fill in your credentials:
   ```bash
   cp .env.template .env
   ```

   Edit `.env` with your actual values:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   XERO_CLIENT_ID=your-xero-client-id-here
   XERO_CLIENT_SECRET=your-xero-client-secret-here
   ```

   **Important:** You must have valid Xero API credentials and an active OpenAI API key for the application to work properly. The application will fail if these are not set or are invalid.

## Running the Application

To start the application:
```bash
npm start
# or
npx ts-node index.ts
```

## Features

The application includes several demo modes:

1. **Basic Agent Demo** - General Xero operations
2. **Invoice Specialist Demo** - Focused on invoice management
3. **Contact Manager Demo** - Contact and customer management
4. **Multi-Agent Workflow** - Demonstrates multiple agents working together
5. **Comprehensive Workflow** - End-to-end business process examples
6. **Interactive Agent** - Chat with an AI agent in real-time

## Available Agents

### General Xero Assistant
- Can perform all Xero operations
- Manages contacts, invoices, and other accounting tasks
- Provides comprehensive help with Xero workflows

### Invoice Specialist
- Specializes in creating, finding, and managing invoices
- Understands invoice workflows and accounting practices
- Always provides invoice numbers and IDs

### Contact Manager
- Focuses on customer and supplier management
- Creates, finds, and updates contact information
- Validates important contact details for accuracy

## Example Operations

- Create customers and suppliers
- Generate invoices with line items
- Search for existing records
- Manage contact information
- Track invoice statuses

## Important Notes

- Contact IDs in Xero are UUIDs (e.g., `12345678-1234-1234-1234-123456789abc`)
- When creating invoices, you need valid contact IDs from existing customers
- The agents will guide you through proper workflows and data requirements

## Troubleshooting

- Ensure your Xero credentials are correct and have appropriate permissions
- Make sure your OpenAI API key is valid and has sufficient credits
- Check that all dependencies are installed correctly with `npm install`

## Development

To run in development mode with automatic restarts:
```bash
npm run dev
```

To run type checking:
```bash
npm run type-check
```