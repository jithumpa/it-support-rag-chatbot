# IT Support Chatbot - Quick Start Guide

## 🚀 Ready to Run!

Your IT Support Chatbot is fully configured and tested. Here's how to get started:

---

## ⚡ Fast Start (5 minutes)

### Option 1: Web UI (Recommended) 🌐

```bash
# Navigate to project directory
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot

# Run Streamlit
streamlit run streamlit.py
```

Then open in browser: **http://localhost:8501**

**Available Features:**
- 💬 Chat with AI assistant about IT issues
- 🎫 Create support tickets
- 🔍 Check ticket status
- 📚 Browse knowledge base

---

### Option 2: Console Chatbot 🖥️

```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
python3 app_implementation.py
```

**Commands:**
```
You: How do I fix WiFi issues?
Chatbot: [Provides IT support answer from knowledge base]

You: create ticket: WiFi not connecting
Chatbot: Ticket created - ID: TKT-20261119185647

You: check ticket: TKT-20261119185647
Chatbot: Ticket status: OPEN

You: quit
[Exits application]
```

---

### Option 3: MCP Server Only 🔧

```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
python3 mcp_server.py
```

Server runs at: **http://localhost:8000**

**Test with curl:**
```bash
# Check health
curl http://localhost:8000/health

# Create ticket
curl -X POST "http://localhost:8000/mcp/create_ticket?issue=WiFi+issue&priority=High"

# Get ticket status
curl "http://localhost:8000/mcp/get_status_ticket/TKT-20261119185647"

# List all tickets
curl "http://localhost:8000/mcp/list_tickets"
```

---

### Option 4: Run Everything (3 Terminals) 🚀

**Terminal 1 - MCP Server:**
```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
python3 mcp_server.py
# Output: Starting server on http://0.0.0.0:8000
```

**Terminal 2 - Streamlit UI:**
```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
streamlit run streamlit.py
# Output: You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

**Terminal 3 - Optional Console:**
```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
python3 app_implementation.py
```

Then access: 
- Web UI: http://localhost:8501
- MCP API: http://localhost:8000
- Console: Type in Terminal 3

---

## 🧪 Verify Everything Works

Run the test suite anytime to verify all components:

```bash
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot
python3 test_all.py
```

**Expected output:**
```
✅ Dependencies: PASSED
✅ Environment: PASSED
✅ RAG System: PASSED
✅ MCP Server: PASSED
✅ All tests passed! Ready to run the application.
```

---

## 📋 What's Working

### ✅ Completed Features

| Feature | Status | File |
|---------|--------|------|
| Streamlit Web UI | ✅ | `streamlit.py` |
| RAG Implementation | ✅ | `app_implementation.py` |
| MCP Server | ✅ | `mcp_server.py` |
| Knowledge Base | ✅ | `it_sector.txt` |
| Ticket Management | ✅ | `mcp_server.py` |
| Chat Mode | ✅ | `streamlit.py` |
| Create Ticket Mode | ✅ | `streamlit.py` |
| Check Ticket Mode | ✅ | `streamlit.py` |
| Knowledge Base Search | ✅ | `streamlit.py` |
| VoyageAI Integration | ✅ | `app_implementation.py` |
| Pinecone Integration | ✅ | `app_implementation.py` |

### 🔧 Configuration

| Item | Status |
|------|--------|
| `.env` file | ✅ Created |
| API Keys | ✅ Setup |
| Dependencies | ✅ All installed |
| Knowledge Base | ✅ Loaded (5159 chars) |

---

## 🛠️ Configuration

### API Keys Setup

The `.env` file is pre-created. Add your API keys:

```bash
# Edit the file
nano .env

# Required:
ANTHROPIC_API_KEY=sk-ant-...your-key-here...

# Optional (for advanced embeddings):
VOYAGE_API_KEY=your-voyage-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-west-1
PINECONE_INDEX_NAME=it-support-kb
```

**Get API Keys:**
- **Anthropic**: https://console.anthropic.com
- **VoyageAI**: https://www.voyageai.com
- **Pinecone**: https://www.pinecone.io

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "API Key error"
1. Check `.env` file exists
2. Add your ANTHROPIC_API_KEY
3. Restart the app

### Streamlit port already in use
```bash
streamlit run streamlit.py --server.port 8502
```

### MCP server port already in use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Embeddings not working
- It's optional! App works with keyword search
- Add VOYAGE_API_KEY and PINECONE_API_KEY to enable

---

## 📚 Project Structure

```
Task2_IT_Support_Chatbot/
├── streamlit.py              # Web UI (Recommended entry point)
├── app_implementation.py      # RAG + Claude AI + Tools
├── mcp_server.py            # FastAPI MCP Server
├── it_sector.txt            # Knowledge base (IT docs)
├── requirements.txt         # Python dependencies
├── .env                     # API configuration
├── .env.example             # Template
├── test_all.py              # Test suite
├── QUICK_START.md           # This file
└── README.md                # Full documentation
```

---

## 🎯 Next Steps

### Option A: Deploy to Production
1. Use a production server (Gunicorn, etc.)
2. Add proper database (PostgreSQL, etc.)
3. Implement user authentication
4. Add email notifications
5. Set up monitoring and logging

### Option B: Enhance Features
1. Add real web search API
2. Implement ticket database persistence
3. Add multi-language support
4. Create mobile app
5. Add analytics dashboard

### Option C: Integration
1. Connect to Jira for ticket sync
2. Integrate with Slack/Teams
3. Add email integration
4. Connect to ticketing system
5. Add webhook support

---

## 💡 Tips

1. **First run?** Use Streamlit UI for best experience
2. **API testing?** Use MCP server endpoints with curl
3. **Console testing?** Use `python3 app_implementation.py`
4. **Multiple terminals?** Run all components simultaneously
5. **Debugging?** Check terminal output for detailed logs

---

## ✨ Feature Showcase

### Chat Mode Demo
```
User: How do I fix slow internet?
Bot: I'd help you troubleshoot slow internet. Here are some steps:
     1. Check bandwidth usage
     2. Run speed test at speedtest.net
     3. Restart your router
     4. Check if MAC filtering is enabled
     5. Contact ISP if issues persist
```

### Ticket Management Demo
```
User: I need to create a support ticket
Bot: Please describe the issue
User: WiFi connection unstable
Bot: ✅ Ticket TKT-20261119185647 created
     Priority: Medium
     Status: OPEN
```

---

## 📞 Support

For detailed information, see:
- **README.md** - Full documentation
- **test_all.py** - Automated testing
- **Code comments** - Implementation details

---

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [VoyageAI Embeddings](https://docs.voyageai.com/)
- [Pinecone Vector DB](https://docs.pinecone.io/)
- [FastAPI Framework](https://fastapi.tiangolo.com/)

---

**Ready to chat?** Run one of the commands above! 🚀
