# Security Guidelines

## 🔐 Credential Management

### **NEVER commit these to git:**
- `.env` files
- API keys or secrets
- Private keys or certificates
- Database passwords
- Any sensitive configuration

### **DO commit these:**
- `.env.example` files with placeholder values
- Documentation about required environment variables
- Security guidelines (like this file)

## 🛡️ Required Environment Variables

All examples in this repository require the following environment variables:

### Xero API Credentials
```bash
XERO_CLIENT_ID=your-xero-client-id-here
XERO_CLIENT_SECRET=your-xero-client-secret-here
```

### AI Service API Keys
Choose one of the following:

**OpenAI (for OpenAI examples):**
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Google AI Studio (for Google ADK examples):**
```bash
GOOGLE_API_KEY=your-google-ai-studio-api-key-here
```

**Google Vertex AI (alternative for Google ADK):**
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

## 🚨 Security Best Practices

### 1. Environment File Setup
1. Copy `.env.example` to `.env` in each project directory
2. Fill in your actual credentials in `.env`
3. **Never** commit `.env` files to version control

### 2. Credential Rotation
- Rotate API keys regularly (every 3-6 months)
- Immediately rotate if you suspect exposure
- Use different keys for development vs production

### 3. Git Safety
- Always check `git status` before committing
- Use `git diff --cached` to review staged changes
- Consider using git hooks to prevent credential commits

### 4. Development Workflow
```bash
# ✅ GOOD: Copy example and fill with real values
cp .env.example .env
# Edit .env with your credentials

# ✅ GOOD: Check what you're committing
git status
git diff --cached

# ❌ BAD: Never do this
git add .env
```

## 🔧 Getting Your API Keys

### Xero Developer Account
1. Go to [Xero Developer Portal](https://developer.xero.com/)
2. Create a new app or use existing one
3. Get your Client ID and Client Secret
4. Configure redirect URI if needed

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new secret key
4. Copy and store securely

### Google AI Studio
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and store securely

## 🚑 What to do if credentials are exposed

### Immediate Actions (Do in this order)
1. **Revoke the exposed credentials immediately**
   - Xero: Regenerate Client Secret in developer portal
   - OpenAI: Delete the exposed API key, create new one
   - Google: Disable the exposed key, create new one

2. **Remove from public repositories**
   - Delete the repository if possible
   - Use git history rewriting tools (BFG Repo-Cleaner)
   - Contact platform support for cache removal

3. **Monitor for abuse**
   - Check usage logs for unauthorized activity
   - Monitor billing for unexpected charges
   - Review access logs

### Prevention
- Use this SECURITY.md as a checklist
- Set up git hooks to prevent credential commits
- Use environment variable managers
- Regular security audits of repositories

## 📝 Security Checklist

Before pushing to any repository:

- [ ] No `.env` files are being committed
- [ ] All `.env.example` files have placeholder values only
- [ ] No hardcoded API keys in source code
- [ ] No private keys or certificates included
- [ ] `.gitignore` properly excludes sensitive files
- [ ] README includes security setup instructions

---

**Remember: It's easier to prevent credential exposure than to clean it up afterward!**