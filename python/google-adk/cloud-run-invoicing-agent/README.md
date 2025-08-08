# Xero Invoicing Agent for Google Cloud Run

A production-ready invoicing agent built with Google's Agent Development Kit (ADK), Xero's Model Context Protocol (MCP) server, and Vertex AI that can be deployed to Google Cloud Run with a single command.

## Overview

This application provides an AI-powered invoicing agent that can:

- **Create and manage invoices** in Xero using natural language
- **Query customer and item data** from your Xero organization
- **Handle tax rates and accounting codes** automatically
- **Provide a web interface** for easy interaction
- **Scale automatically** on Google Cloud Run
- **Deploy in minutes** with simple commands

The agent uses Google's ADK framework to provide a robust conversational interface, integrating seamlessly with Xero's accounting platform through the MCP protocol.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Client    │───▶│  FastAPI + ADK   │───▶│   Xero MCP      │
│                 │    │   (Cloud Run)    │    │   Server        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                       ┌─────────────┐           ┌─────────────┐
                       │ Vertex AI   │           │   Xero API  │
                       │   Models    │           │             │
                       └─────────────┘           └─────────────┘
```

## Features

- **🚀 One-command deployment** to Google Cloud Run
- **💬 Natural language interface** for invoice creation
- **🔧 Comprehensive Xero integration** (contacts, items, invoices, tax rates)
- **🌐 Built-in web UI** for easy testing and interaction
- **📊 Session management** with SQLite database
- **🔒 Secure environment variable handling**
- **📈 Auto-scaling** and serverless architecture
- **🐳 Containerized** with Docker for consistent deployment

## Prerequisites

Before you begin, ensure you have:

### 1. Development Tools
- **Node.js** (v18+) and **npm** - Required for Xero MCP Server
- **Python** (3.12+) - For the application runtime
- **Google Cloud CLI** - For deployment to Cloud Run

### 2. Accounts & Credentials
- **Xero Developer Account** - Get credentials from [Xero Developer Portal](https://developer.xero.com/)
  - Client ID
  - Client Secret
- **Google Cloud Project** - With Cloud Run API enabled
- **Vertex AI** - Enabled in your Google Cloud project

### 3. Permissions
Ensure your Google Cloud account has:
- Cloud Run Developer role
- Service Account User role
- Vertex AI User role

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd python/google-adk/cloud-run-invoicing-agent

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Xero API Credentials
XERO_CLIENT_ID=your_xero_client_id_here
XERO_CLIENT_SECRET=your_xero_client_secret_here

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=true

# Agent Configuration
DEFAULT_MODEL=gemini-1.5-flash
AGENT_SERVICE_NAME=xero-invoicing-agent
```

### 3. Test Locally (Optional)

```bash
# Run the application locally
python main.py

# Visit http://localhost:8000 to access the web interface
```

### 4. Deploy to Cloud Run

```bash
# Deploy with a single command
make deploy
```

That's it! Your invoicing agent is now running on Google Cloud Run.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `XERO_CLIENT_ID` | Your Xero application client ID | ✅ | - |
| `XERO_CLIENT_SECRET` | Your Xero application client secret | ✅ | - |
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID | ✅ | - |
| `GOOGLE_CLOUD_LOCATION` | GCP region for deployment | ✅ | `us-central1` |
| `DEFAULT_MODEL` | Vertex AI model to use | ❌ | `gemini-1.5-flash` |
| `AGENT_SERVICE_NAME` | Cloud Run service name | ❌ | `xero-invoicing-agent` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI instead of AI Studio | ❌ | `true` |

### Supported Xero Operations

The agent has access to these Xero MCP tools:

- `list-contacts` - Retrieve customer/supplier information
- `list-items` - Get product/service catalog
- `list-tax-rates` - Fetch available tax rates
- `list-accounts` - Access chart of accounts
- `list-tracking-categories` - Get tracking categories
- `create-invoice` - Create new invoices
- `list-invoices` - Query existing invoices
- `update-invoice` - Modify draft invoices

## Usage Examples

### Creating an Invoice

Once deployed, you can interact with the agent using natural language:

```
User: "Create an invoice for Acme Corp for 3 consulting hours at $150/hour"

Agent: I'll help you create that invoice. Let me first check for Acme Corp in your contacts and get the appropriate account codes...

[Agent proceeds to:]
1. Search for "Acme Corp" in contacts
2. Look up appropriate account codes for consulting services
3. Apply correct tax rates
4. Create the invoice with line items
5. Provide the invoice details and Xero link
```

### Querying Information

```
User: "Show me all unpaid invoices from last month"

Agent: I'll retrieve your unpaid invoices from last month...

[Agent provides a formatted list of unpaid invoices with amounts and due dates]
```

## Deployment Commands

### Deploy
```bash
make deploy
```

### Delete Service
```bash
make delete
```

### View Logs
```bash
gcloud run services logs read xero-invoicing-agent \
  --region=us-central1 \
  --project=your-project-id
```

### Update Environment Variables
```bash
gcloud run services update xero-invoicing-agent \
  --region=us-central1 \
  --project=your-project-id \
  --set-env-vars="NEW_VAR=value"
```

## Development

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run locally:**
   ```bash
   python main.py
   ```

4. **Access the application:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Project Structure

```
cloud-run-invoicing-agent/
├── main.py                 # FastAPI application entry point
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies
├── makefile              # Deployment commands
├── .env                  # Environment variables (create this)
└── xero_invoicing_agent/
    ├── __init__.py
    ├── agent.py          # Main agent configuration
    └── config.py         # Application settings
```

### Key Components

- **`main.py`** - FastAPI application setup with ADK integration
- **`agent.py`** - Agent definition with Xero MCP toolset and instructions
- **`config.py`** - Configuration management for Vertex AI and other settings
- **`Dockerfile`** - Multi-stage build with Node.js and Python
- **`makefile`** - Simplified deployment commands

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Ensure you're in the correct directory and have installed dependencies
pip install -r requirements.txt
```

**2. Xero authentication errors**
- Verify your `XERO_CLIENT_ID` and `XERO_CLIENT_SECRET` are correct
- Ensure your Xero app has the necessary scopes enabled

**3. Cloud Run deployment fails**
- Check that Cloud Run API is enabled in your GCP project
- Verify your gcloud CLI is authenticated: `gcloud auth login`
- Ensure you have the necessary IAM roles

**4. Agent not responding**
- Check Cloud Run logs: `gcloud run services logs read xero-invoicing-agent`
- Verify Vertex AI is enabled in your project
- Check environment variables are set correctly

### Getting Help

1. **Check the logs:**
   ```bash
   gcloud run services logs read xero-invoicing-agent \
     --region=us-central1 \
     --project=your-project-id \
     --limit=50
   ```

2. **Test locally first:**
   - Run the application locally to isolate deployment issues
   - Use the `/docs` endpoint to test the API directly

3. **Verify Xero connectivity:**
   - Test your Xero credentials with a simple API call
   - Ensure your Xero organization is properly configured

## Security Considerations

- **Environment Variables**: Never commit `.env` files to version control
- **IAM Roles**: Use principle of least privilege for service accounts
- **Network Security**: Cloud Run services are HTTPS-only by default
- **Secrets Management**: Consider using Google Secret Manager for production

## Cost Optimization

- **Concurrency**: Adjust Cloud Run concurrency settings based on your workload
- **CPU Allocation**: Tune CPU allocation for your specific use case  
- **Min Instances**: Set to 0 for cost optimization (cold starts acceptable)
- **Request Timeout**: Configure appropriate timeout values

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally and on Cloud Run
5. Submit a pull request

## License

This project is part of the xero-agent-toolkit and follows the same licensing terms.

---

## Related Resources

- [Google Agent Development Kit Documentation](https://cloud.google.com/agent-development-kit)
- [Xero MCP Server](https://github.com/xeroapi/xero-mcp-server)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Xero Developer Portal](https://developer.xero.com/)

For more examples and advanced configurations, see the parent [README](../README.md) in the google-adk directory.
