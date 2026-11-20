# TASK 2: IT Support Chatbot

An advanced Streamlit web application providing IT support with RAG (Retrieval-Augmented Generation), MCP server for ticket management, and intelligent knowledge base retrieval.

## Features

### 1. **Streamlit Web UI** (`streamlit.py`)
- Interactive chat interface
- Ticket creation and management
- Knowledge base search and browsing
- Real-time response generation

### 2. **RAG Implementation** (`app_implementation.py`)
- VoyageAI embeddings integration
- Vector database for knowledge retrieval
- Intelligent document ranking
- Context-aware responses

### 3. **MCP Server** (`mcp_server.py`)
- RESTful API endpoints
- Ticket creation: `POST /mcp/create_ticket`
- Ticket status check: `GET /mcp/get_status_ticket/{ticket_id}`
- Ticket listing and filtering
- FastAPI with async support

### 4. **Knowledge Base** (`it_sector.txt`)
- Comprehensive IT support documentation
- Network troubleshooting guides
- Email configuration help
- Security and backup procedures
- Printer and software installation guides

## Architecture

```
┌─────────────────────────────────────┐
│   Streamlit Web UI (streamlit.py)   │
│   - Chat Interface                   │
│   - Ticket Management                │
│   - Knowledge Base Search            │
└─────────────────┬───────────────────┘
                  │
         ┌────────▼────────┐
         │   RAG System    │
         │  (app_impl.py)  │
         │                 │
         │ - Embeddings    │
         │ - Retrieval     │
         │ - LLM Integration
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │   Claude API    │
         │ (Anthropic)     │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │   MCP Server    │
         │  (mcp_server.py)│
         │                 │
         │ - Tickets DB    │
         │ - API Endpoints │
         └─────────────────┘
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+ installed
- API Keys from:
  - [Anthropic Console](https://console.anthropic.com) - **Required**
  - [VoyageAI](https://www.voyageai.com) - Optional (for embeddings)
  - [Pinecone](https://www.pinecone.io) - Optional (for vector DB)

### 2. Install Dependencies
```bash
# Navigate to project directory
cd /Users/aswajithmalayamparambath/Desktop/Task2_IT_Support_Chatbot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
nano .env
# or use your preferred editor (VSCode, vim, etc.)
```

**Required in `.env`:**
```bash
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

**Optional in `.env` (for advanced RAG):**
```bash
VOYAGE_API_KEY=your-voyage-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-west-1
PINECONE_INDEX_NAME=it-support-kb
```

**Note**: The app works with just `ANTHROPIC_API_KEY`. Without VoyageAI/Pinecone, it uses keyword-based search.

### 4. Run the Application

#### Option A: Run Streamlit Web UI
```bash
streamlit run streamlit.py
```
Access at: http://localhost:8501

#### Option B: Run Console RAG Interface
```bash
python app_implementation.py
```

#### Option C: Run MCP Server Only
```bash
python mcp_server.py
```
API available at: http://localhost:8000

#### Option D: Run All Components
```bash
# Terminal 1: MCP Server
python mcp_server.py

# Terminal 2: Streamlit UI
streamlit run streamlit.py
```

## Usage Examples

### Web UI - Chat Mode
```
User: "I can't connect to WiFi"
Bot: "I'd be happy to help! Let me check our knowledge base... 
      First, let's try these steps:
      1. Check if WiFi is enabled
      2. Verify password
      3. Restart the router..."
```

### Web UI - Create Ticket
1. Switch to "Create Ticket" mode
2. Fill in issue title and description
3. Select priority level
4. Click "Create Ticket"
5. Receive ticket ID for tracking

### Web UI - Check Ticket
1. Switch to "Check Ticket" mode
2. Enter ticket ID
3. View current status and details

### Console RAG Interface
```
You: What is my current date and time?
Chatbot: [Retrieved from tools] The current date and time is 2026-11-19 14:30:45

You: create ticket: Cannot access email
Chatbot: Ticket created - ID: TKT-20261119143045

You: check ticket: TKT-20261119143045
Chatbot: Ticket TKT-20261119143045 Status: In Progress
```

### MCP API Endpoints

#### Create Ticket
```bash
curl -X POST "http://localhost:8000/mcp/create_ticket" \
  -H "Content-Type: application/json" \
  -d '{"issue":"WiFi not working","priority":"High","description":"Cannot connect to office WiFi"}'
```

#### Get Ticket Status
```bash
curl "http://localhost:8000/mcp/get_status_ticket/TKT-20261119143045"
```

#### List All Tickets
```bash
curl "http://localhost:8000/mcp/list_tickets"
```

## File Structure
```
Task2_IT_Support_Chatbot/
├── streamlit.py              # Web UI
├── app_implementation.py      # RAG system
├── mcp_server.py             # MCP API server
├── it_sector.txt             # Knowledge base
├── requirements.txt          # Dependencies
├── .env.example              # API key template
└── README.md                 # This file
```

## Configuration

### Knowledge Base
Edit `it_sector.txt` to add or update IT support documentation.

### RAG Settings (streamlit.py)
- Temperature: Controls response creativity (0.0-1.0)
- Max Tokens: Maximum response length

### MCP Server Configuration (mcp_server.py)
- Default host: 0.0.0.0
- Default port: 8000
- Database: In-memory (modify for persistent storage)

## Tools Available

### Client-side Tools
- `get_current_datetime()` - Get current date/time
- `web_search(query)` - Perform web search

### Server-side Tools (MCP)
- `create_ticket(issue, priority, description)` - Create support ticket
- `get_status_ticket(ticket_id)` - Check ticket status
- `update_ticket_status(ticket_id, status)` - Update ticket status
- `list_tickets(status)` - List filtered tickets

## Advanced Features

### RAG Implementation Details
1. **Document Retrieval**: Keyword matching with relevance ranking
2. **Context Window**: Maintains multi-turn conversation history
3. **Embeddings**: Ready for VoyageAI integration
4. **Knowledge Base**: Semantic search across IT documentation

### Ticket Management
- Automatic ID generation (TKT-YYYYMMDDHHMMSS)
- Priority-based organization
- Status tracking (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- Creation and update timestamps

### Web Interface Modes
1. **Chat**: Conversational support
2. **Create Ticket**: Issue tracking
3. **Check Ticket**: Status monitoring
4. **Knowledge Base**: Documentation browsing

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Create `.env` file with your API key
- Ensure file is in the same directory as scripts

### Streamlit port already in use
```bash
streamlit run streamlit.py --server.port 8501
```

### MCP Server port conflict
```bash
python mcp_server.py --port 8001
```

## Next Steps

After completing both tasks:
1. Create a public GitHub repository
2. Push both Task1 and Task2 projects
3. Submit solutions via the form: https://forms.gle/5goNYHRXcFZM34PKA

## Support

For issues or questions:
1. Check the knowledge base in-app
2. Review error messages for specific guidance
3. Ensure all dependencies are installed
4. Verify API keys are configured correctly

---
**IT Support Chatbot | Powered by Claude AI | RAG with VoyageAI Embeddings**
