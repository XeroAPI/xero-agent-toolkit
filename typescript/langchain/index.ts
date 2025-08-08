#!/usr/bin/env node
/**
 * LangChain Integration with Xero MCP Server (TypeScript Version)
 *
 * This example demonstrates advanced use cases for the Xero MCP server
 * with LangChain, including specialized agents, complex workflows,
 * and various integration patterns using the @langchain/mcp-adapters library.
 */

import * as dotenv from 'dotenv';
import * as readline from 'readline';

// Load environment variables from a .env file
dotenv.config();

// Standard LangChain imports
import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { HumanMessage } from '@langchain/core/messages';
import { BaseMessage } from '@langchain/core/messages';

// MCP adapter imports
import { MultiServerMCPClient } from '@langchain/mcp-adapters';

/**
 * Creates a LangChain agent configured to use the Xero MCP Server.
 * @returns A promise that resolves to an object containing the agent and the MCP client.
 */
async function createXeroMcpAgent() {
    // Check for required environment variables
    const xeroClientId = process.env.XERO_CLIENT_ID;
    const xeroClientSecret = process.env.XERO_CLIENT_SECRET;
    
    if (!xeroClientId || !xeroClientSecret) {
        throw new Error('XERO_CLIENT_ID and XERO_CLIENT_SECRET environment variables are required');
    }

    // Configure the MCP client
    const client = new MultiServerMCPClient({
        xero: {
            transport: 'stdio', // or "sse" for HTTP transport
            command: 'npx',
            args: ['-y', '@xeroapi/xero-mcp-server@latest'],
            env: {
                XERO_CLIENT_ID: xeroClientId,
                XERO_CLIENT_SECRET: xeroClientSecret,
            },
        },
    });

    // Get tools automatically - no manual tool wrapping needed!
    const tools = await client.getTools();

    // Create LLM - using GPT-4o for its large context window and reasoning capabilities
    const llm = new ChatOpenAI({ temperature: 0, model: 'gpt-4o' });

    // Create agent using the standard LangGraph approach
    const agent = createReactAgent({ llm, tools });

    return { agent, client };
}

/**
 * Helper function to print the last message from an agent response.
 * @param response - The response object from the agent invocation.
 * @param prefix - A prefix string for the log message (e.g., "✅ Response:").
 */
function printLastMessage(response: { messages: BaseMessage[] }, prefix: string) {
    if (response && Array.isArray(response.messages) && response.messages.length > 0) {
        const lastMessage = response.messages[response.messages.length - 1];
        console.log(`\n${prefix} ${lastMessage.content}`);
    }
}

/**
 * Demonstrates an agent that specializes in invoice operations.
 */
async function demoInvoiceSpecialistAgent() {
    console.log('\n' + '='.repeat(50));
    console.log('INVOICE SPECIALIST AGENT');
    console.log('='.repeat(50));

    const { agent } = await createXeroMcpAgent();

    // Example queries - more focused and realistic
    const queries = [
        'Find all draft invoices',
        'Find the first 3 customers',
        'Create an invoice for one of the customers found for 10 hours of consulting at $150 per hour',
    ];

    try {
        for (const query of queries) {
            console.log(`\n📝 Query: ${query}`);
            const response = await agent.invoke({
                messages: [new HumanMessage({ content: query })],
            });
            printLastMessage(response, '✅ Response:');
        }
    } catch (e) {
        console.error(`\n❌ Error:`, e);
    }
}

/**
 * Demonstrates an agent that manages contacts.
 */
async function demoContactManagerAgent() {
    console.log('\n' + '='.repeat(50));
    console.log('CONTACT MANAGER AGENT');
    console.log('='.repeat(50));

    const { agent } = await createXeroMcpAgent();

    const queries = [
        "Create a new customer called 'Demo Corp' with email demo@demo.com",
        'Find all suppliers',
        "Search for contacts with 'demo' in their name",
    ];

    try {
        for (const query of queries) {
            console.log(`\n📝 Query: ${query}`);
            const response = await agent.invoke({
                messages: [new HumanMessage({ content: query })],
            });
            printLastMessage(response, '✅ Response:');
        }
    } catch (e) {
        console.error(`\n❌ Error:`, e);
    }
}

/**
 * Demonstrates a multi-step workflow.
 */
async function demoMultiStepWorkflow() {
    console.log('\n' + '='.repeat(50));
    console.log('MULTI-STEP WORKFLOW: MONTHLY INVOICING');
    console.log('='.repeat(50));

    const { agent } = await createXeroMcpAgent();

    const workflowPrompt = `
    Please help me with monthly invoicing:
    1. First, find all active customers
    2. Show me the first 3 customers found
    3. Explain how I could create invoices for them (but don't actually create them yet)
    `;

    console.log(`\n📋 Workflow Request: ${workflowPrompt}`);

    try {
        const response = await agent.invoke({
            messages: [new HumanMessage({ content: workflowPrompt })],
        });
        printLastMessage(response, '✅ Workflow Result:');
    } catch (e) {
        console.error(`\n❌ Error:`, e);
    }
}

/**
 * Demonstrates invoice analysis.
 */
async function demoInvoiceAnalysis() {
    console.log('\n' + '='.repeat(50));
    console.log('INVOICE ANALYSIS');
    console.log('='.repeat(50));

    const { agent } = await createXeroMcpAgent();

    const analysisPrompt = `
    Please help me analyze my invoices:
    1. Find a recent invoice
    2. Provide analysis including total amount, payment status, and any recommendations
    3. If overdue, calculate days overdue
    `;

    console.log(`\n📊 Analysis Request: ${analysisPrompt}`);

    try {
        const response = await agent.invoke({
            messages: [new HumanMessage({ content: analysisPrompt })],
        });
        printLastMessage(response, '✅ Analysis Result:');
    } catch (e) {
        console.error(`\n❌ Error:`, e);
    }
}

/**
 * Demonstrates getting organization insights.
 */
async function demoOrganizationInsights() {
    console.log('\n' + '='.repeat(50));
    console.log('ORGANIZATION INSIGHTS');
    console.log('='.repeat(50));

    const { agent } = await createXeroMcpAgent();

    const insightsPrompt = `
    Please provide me with insights about my Xero organization:
    1. Get the organization details
    2. Get a summary of contacts (total count, types)
    3. Get a summary of recent invoices
    4. Provide any recommendations for better organization
    `;

    console.log(`\n📈 Insights Request: ${insightsPrompt}`);

    try {
        const response = await agent.invoke({
            messages: [new HumanMessage({ content: insightsPrompt })],
        });
        printLastMessage(response, '✅ Insights:');
    } catch (e) {
        console.error(`\n❌ Error:`, e);
    }
}

/**
 * Runs an interactive demo with the Xero agent.
 */
async function interactiveMcpDemo() {
    console.log('\n' + '='.repeat(50));
    console.log('INTERACTIVE XERO AGENT');
    console.log('='.repeat(50));
    console.log("\nChat with your Xero agent. The agent has access to all Xero functions.");
    console.log("Type 'quit' or 'exit' to end the session.\n");

    const { agent } = await createXeroMcpAgent();
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    const chat = async () => {
        rl.question('\n👤 You: ', async (userInput) => {
            if (userInput.toLowerCase() === 'quit' || userInput.toLowerCase() === 'exit') {
                console.log('\n🤖 Assistant: Goodbye!');
                rl.close();
                return;
            }

            if (!userInput.trim()) {
                chat();
                return;
            }

            try {
                const response = await agent.invoke({
                    messages: [new HumanMessage({ content: userInput })],
                });
                printLastMessage(response, '🤖 Assistant:');
            } catch (e) {
                console.error(`\n❌ Error:`, e);
            }
            chat(); // Continue the loop
        });
    };

    await chat();
}

/**
 * Main function to run the MCP integration examples.
 */
async function main() {
    // Check for required environment variables
    if (!process.env.OPENAI_API_KEY) {
        console.error('Error: OPENAI_API_KEY not set in environment.');
        return;
    }

    if (!process.env.XERO_CLIENT_ID || !process.env.XERO_CLIENT_SECRET) {
        console.error('Error: Xero credentials not set in environment.');
        console.error('Please set XERO_CLIENT_ID and XERO_CLIENT_SECRET in a .env file.');
        return;
    }

    console.log('LangChain + Xero MCP Integration Examples (TypeScript)');
    console.log('====================================================\n');

    const demos: { [key: string]: () => Promise<void> } = {
        '1': demoInvoiceSpecialistAgent,
        '2': demoContactManagerAgent,
        '3': demoMultiStepWorkflow,
        '4': demoInvoiceAnalysis,
        '5': interactiveMcpDemo,
        '6': demoOrganizationInsights,
    };

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    console.log('Select a demo:');
    Object.keys(demos).forEach((key) => {
        // Extract function name, remove "demo", and format it
        const name = demos[key].name.replace('demo', '').replace(/([A-Z])/g, ' $1').trim();
        console.log(`${key}. ${name}`);
    });

    rl.question('\nEnter your choice (1-6): ', async (choice) => {
        const selectedDemo = demos[choice.trim()];
        if (selectedDemo) {
            await selectedDemo();
            // Close readline interface if not the interactive demo
            if (choice.trim() !== '5') {
                rl.close();
            }
        } else {
            console.log('Invalid choice. Please run again and select a number from 1-6.');
            rl.close();
        }
    });
}

// Execute the main function
main().catch(console.error);