#!/usr/bin/env ts-node
/**
 * OpenAI Agents SDK Integration Example (TypeScript Version)
 *
 * This example demonstrates how to use the Xero MCP Server
 * with the OpenAI Agents SDK to create AI agents that can
 * manage Xero accounting operations.
 *
 * To run this file:
 * 1. Make sure you have Node.js and npm installed.
 * 2. Install dependencies:
 * npm install @openai/agents dotenv ts-node typescript command-exists
 * 3. Create a .env file in the same directory with your keys:
 * OPENAI_API_KEY="sk-..."
 * XERO_CLIENT_ID="..."
 * XERO_CLIENT_SECRET="..."
 * 4. Run the script:
 * npx ts-node ./your_script_name.ts
 */

import 'dotenv/config';
import {
  Agent,
  Runner,
  generateTraceId,
  getCurrentTrace,
  MCPServerStdio,
  run,
} from '@openai/agents';
import * as readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { sync as commandExistsSync } from 'command-exists';

/**
 * Creates a basic Xero agent with all tools.
 * @param mcpServer The MCP server instance for Xero.
 * @returns A configured Agent instance.
 */
function createBasicXeroAgent(mcpServer: MCPServerStdio): Agent {
  return new Agent({
    name: 'Xero Assistant',
    model: 'gpt-4o-mini',
    instructions: `You are a helpful accounting assistant that manages Xero operations. 
        You can create invoices, manage contacts, search for records, and handle various 
        accounting tasks. Always confirm successful operations and provide relevant details 
        to the user. Be precise with data handling and always verify important information.`,
    mcpServers: [mcpServer],
  });
}

/**
 * Creates an agent that specializes in invoice operations.
 * @param mcpServer The MCP server instance for Xero.
 * @returns A configured Agent instance for invoice operations.
 */
function createInvoiceSpecialistAgent(mcpServer: MCPServerStdio): Agent {
  return new Agent({
    name: 'Invoice Specialist',
    model: 'gpt-4o-mini',
    instructions: `You are an invoice specialist for Xero. You excel at creating, 
        finding, and managing invoices. You understand accounting practices and can help 
        with invoice workflows. Always provide invoice numbers and IDs when creating or 
        finding invoices.`,
    mcpServers: [mcpServer],
  });
}

/**
 * Creates an agent that specializes in contact management.
 * @param mcpServer The MCP server instance for Xero.
 * @returns A configured Agent instance for contact operations.
 */
function createContactManagerAgent(mcpServer: MCPServerStdio): Agent {
  return new Agent({
    name: 'Contact Manager',
    model: 'gpt-4o-mini',
    instructions: `You are a contact management specialist for Xero. You help create, 
        find, and update customer and supplier information. You understand the importance 
        of accurate contact data for accounting and always validate important details.`,
    mcpServers: [mcpServer],
  });
}

/**
 * Demonstrates the basic Xero agent's capabilities.
 */
async function demoBasicAgent(mcpServer: MCPServerStdio): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('BASIC XERO AGENT DEMO');
  console.log('='.repeat(60));

  const agent = createBasicXeroAgent(mcpServer);

  const requests = [
    'Find all active customers',
    "Create a new customer named 'Tech Solutions Inc' with email tech@solutions.com",
    "Find customers with 'Tech' in their name to see if our customer was created",
  ];

  for (const request of requests) {
    console.log(`\n🤖 User: ${request}`);
    console.log('💭 Agent thinking...');

    try {
      const result = await run(agent, request);
      console.log(`✅ Agent: ${result.finalOutput}`);
    } catch (e) {
      console.error(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  console.log('\n💡 Note: To create an invoice, you would need to:');
  console.log('    1. First get the contact_id from the customer creation response');
  console.log('    2. Then create an invoice using that specific contact_id');
  console.log("    3. Contact IDs in Xero are UUIDs, not simple strings like 'abc123'");
}

/**
 * Demonstrates the invoice specialist agent.
 */
async function demoInvoiceSpecialist(mcpServer: MCPServerStdio): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('INVOICE SPECIALIST AGENT DEMO');
  console.log('='.repeat(60));

  const agent = createInvoiceSpecialistAgent(mcpServer);

  const requests = [
    'Find all draft invoices',
    'Find all invoices with status AUTHORISED',
    'Find invoices from the last 30 days',
  ];

  for (const request of requests) {
    console.log(`\n📝 User: ${request}`);
    console.log('💭 Agent thinking...');

    try {
      const result = await run(agent, request);
      console.log(`✅ Agent: ${result.finalOutput}`);
    } catch (e) {
      console.error(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }
}

/**
 * Demonstrates the contact manager agent.
 */
async function demoContactManager(mcpServer: MCPServerStdio): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('CONTACT MANAGER AGENT DEMO');
  console.log('='.repeat(60));

  const agent = createContactManagerAgent(mcpServer);

  const requests = [
    'Find all customers',
    "Create a new supplier 'Office Supplies Ltd' with email orders@officesupplies.com",
    "Search for contacts with 'tech' in their name",
  ];

  for (const request of requests) {
    console.log(`\n👥 User: ${request}`);
    console.log('💭 Agent thinking...');

    try {
      const result = await run(agent, request);
      console.log(`✅ Agent: ${result.finalOutput}`);
    } catch (e) {
      console.error(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }
}

/**
 * Demonstrates a workflow using multiple specialized agents.
 */
async function demoMultiAgentWorkflow(mcpServer: MCPServerStdio): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('MULTI-AGENT WORKFLOW DEMO');
  console.log('='.repeat(60));

  const contactAgent = createContactManagerAgent(mcpServer);

  console.log('\n🔄 Step 1: Contact Manager creates a new customer');
  try {
    const result1 = await run(contactAgent, "Create a new customer named 'Demo Corp' with email billing@democorp.com");
    console.log(`✅ Contact Agent: ${result1.finalOutput}`);

    console.log('\n🔄 Step 2: Find the customer we just created');
    const result2 = await run(contactAgent, "Find a customer named 'Demo Corp'");
    console.log(`✅ Contact Agent: ${result2.finalOutput}`);

    console.log('\n🔄 Step 3: Find existing customers to create an invoice for');
    const result3 = await run(contactAgent, 'Find the first 3 customers');
    console.log(`✅ Contact Agent: ${result3.finalOutput}`);

    console.log('\n💡 Note: In a real application, you would extract the contact ID');
    console.log('    from the contact creation response and pass it to the invoice agent.');
  } catch (e) {
    console.error(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
  }
}

/**
 * Demonstrates a comprehensive end-to-end workflow.
 */
async function demoComprehensiveWorkflow(mcpServer: MCPServerStdio): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('COMPREHENSIVE WORKFLOW DEMO');
  console.log('='.repeat(60));
  console.log('This demo shows how to properly work with contact IDs and create invoices');

  const agent = createBasicXeroAgent(mcpServer);

  console.log('\n🔄 Step 1: Create a new customer');
  try {
    const result1 = await run(agent, "Create a new customer named 'Workflow Demo Ltd' with email demo@workflow.com");
    console.log(`✅ Agent: ${result1.finalOutput}`);

    console.log('\n🔄 Step 2: Find customers to get a valid contact ID');
    const result2 = await run(agent, "Find customers with 'Workflow' in their name and show me their contact IDs");
    console.log(`✅ Agent: ${result2.finalOutput}`);

    console.log('\n🔄 Step 3: Search for any existing customers we can use');
    const result3 = await run(agent, 'Find the first 3 customers and show their contact IDs so I can create an invoice');
    console.log(`✅ Agent: ${result3.finalOutput}`);

    console.log('\n💡 Instructions for creating an invoice:');
    console.log('    1. Copy one of the contact IDs from above (the UUID format)');
    console.log('    2. Use that ID to create an invoice like this:');
    console.log("       'Create an invoice for contact ID [paste-uuid-here] with line item: Consulting for $1000'");
    console.log('    3. The contact ID must be in UUID format like: 12345678-1234-1234-1234-123456789abc');
  } catch (e) {
    console.error(`❌ Error: ${e instanceof Error ? e.message : String(e)}`);
  }
}

/**
 * Runs an interactive demo with the Agents SDK.
 */
async function interactiveDemo(mcpServer: MCPServerStdio): Promise<void> {
  const rl = readline.createInterface({ input, output });

  console.log('\n' + '='.repeat(60));
  console.log('INTERACTIVE XERO AGENTS SDK DEMO');
  console.log('='.repeat(60));
  console.log('\nChoose an agent type:');
  console.log('1. General Xero Assistant (all tools)');
  console.log('2. Invoice Specialist');
  console.log('3. Contact Manager');

  const choice = await rl.question('\nEnter your choice (1-3): ');
  let agent: Agent;
  let agentName: string;

  switch (choice.trim()) {
    case '1':
      agent = createBasicXeroAgent(mcpServer);
      agentName = 'General Assistant';
      break;
    case '2':
      agent = createInvoiceSpecialistAgent(mcpServer);
      agentName = 'Invoice Specialist';
      break;
    case '3':
      agent = createContactManagerAgent(mcpServer);
      agentName = 'Contact Manager';
      break;
    default:
      console.log('Invalid choice.');
      rl.close();
      return;
  }

  console.log(`\n🤖 ${agentName} is ready!`);
  console.log('\nType your requests in natural language.');
  console.log('Examples:');
  console.log("- 'Create a new customer named ABC Corp with email info@abc.com'");
  console.log("- 'Find all customers'");
  console.log("- 'Find all draft invoices'");
  console.log("- 'Find customers and show their contact IDs'");
  console.log('\n⚠️  Important for creating invoices:');
  console.log('- Contact IDs must be in UUID format (e.g., 12345678-1234-1234-1234-123456789abc)');
  console.log("- Use 'Find customers' first to get valid contact IDs");
  console.log("- Then use: 'Create invoice for contact ID [uuid] with item: Description for $Amount'");
  console.log("\nType 'quit' to exit.\n");

  while (true) {
    try {
      const userInput = await rl.question('\nYou: ');
      if (['quit', 'exit', 'q'].includes(userInput.toLowerCase().trim())) {
        console.log('\nGoodbye!');
        break;
      }
      if (!userInput.trim()) {
        continue;
      }

      console.log('💭 Agent thinking...');
      const result = await run(agent, userInput);
      console.log(`\n🤖 ${agentName}: ${result.finalOutput}`);
    } catch (e) {
      if (e instanceof Error && e.constructor.name === 'ReadlineError') {
        // This handles Ctrl+C gracefully
        console.log('\n\nGoodbye!');
        break;
      }
      console.error(`\n❌ Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }
  rl.close();
}

/**
 * Runs the selected demo with the MCP server.
 */
async function runDemoWithMcp(mcpServer: MCPServerStdio): Promise<void> {
  const rl = readline.createInterface({ input, output });

  console.log('Xero + OpenAI Agents SDK Integration Examples');
  console.log('='.repeat(50));

  console.log('\nSelect a demo:');
  console.log('1. Basic Agent Demo');
  console.log('2. Invoice Specialist Demo');
  console.log('3. Contact Manager Demo');
  console.log('4. Multi-Agent Workflow');
  console.log('5. Comprehensive Workflow (Recommended)');
  console.log('6. Interactive Agent');

  const choice = await rl.question('\nEnter your choice (1-6): ');
  rl.close(); // Close the readline interface after getting the choice

  switch (choice.trim()) {
    case '1':
      await demoBasicAgent(mcpServer);
      break;
    case '2':
      await demoInvoiceSpecialist(mcpServer);
      break;
    case '3':
      await demoContactManager(mcpServer);
      break;
    case '4':
      await demoMultiAgentWorkflow(mcpServer);
      break;
    case '5':
      await demoComprehensiveWorkflow(mcpServer);
      break;
    case '6':
      // Interactive demo has its own readline instance, so we don't pass one
      await interactiveDemo(mcpServer);
      break;
    default:
      console.log('Invalid choice. Please run again and select 1-6.');
  }
}

/**
 * Main function to run the OpenAI Agents SDK integration examples.
 */
async function main() {
  // Check for required environment variables
  if (!process.env.OPENAI_API_KEY) {
    console.error('Error: OPENAI_API_KEY not set in environment');
    console.error('Please set your OpenAI API key to run this example');
    return;
  }
  if (!process.env.XERO_CLIENT_ID || !process.env.XERO_CLIENT_SECRET) {
    console.error('Error: Xero credentials not set in environment');
    console.error('Please set XERO_CLIENT_ID and XERO_CLIENT_SECRET');
    return;
  }

  // Check if npx is available
  if (!commandExistsSync('npx')) {
    throw new Error('npx is not installed. Please install it with `npm install -g npx`.');
  }

  // Initialize MCP server
  const server = new MCPServerStdio({
    name: 'Xero',
    command: 'npx',
    args: ['-y', '@xeroapi/xero-mcp-server@latest'],
    env: {
      XERO_CLIENT_ID: process.env.XERO_CLIENT_ID,
      XERO_CLIENT_SECRET: process.env.XERO_CLIENT_SECRET,
    },
  });

  try {
    // Connect to the MCP server
    console.log('Connecting to Xero MCP server...');
    await server.connect();
    console.log('✅ Connected to Xero MCP server successfully!\n');

    const traceId = generateTraceId();
    console.log(`View trace: https://platform.openai.com/traces/${traceId}\n`);

    // Run demos
    await runDemoWithMcp(server);
  } catch (err) {
    console.error('An error occurred during execution:', err);
  } finally {
    // Ensure the server is properly closed
    try {
      await server.close();
      console.log('✅ MCP server connection closed.');
    } catch (closeErr) {
      console.error('Error closing MCP server:', closeErr);
    }
  }
}

// Execute the main function
main().catch(console.error);
