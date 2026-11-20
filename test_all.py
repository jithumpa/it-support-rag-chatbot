#!/usr/bin/env python3
"""
IT Support Chatbot - Quick Test & Demo Script
Tests all components and demonstrates usage
"""

import sys
import subprocess
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def test_dependencies():
    """Test if all required dependencies are installed"""
    print_section("TESTING DEPENDENCIES")
    
    required_packages = {
        "anthropic": "anthropic",
        "voyageai": "voyageai",
        "pinecone": "pinecone",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "pydantic": "pydantic",
        "requests": "requests",
        "dotenv": "python-dotenv"
    }
    
    missing = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print_success(f"{package_name}")
        except ImportError:
            print_warning(f"{package_name} - not installed")
            missing.append(package_name)
    
    # Note: Streamlit is not tested here due to naming conflict with streamlit.py
    print_success("streamlit (not checked to avoid import conflict)")
    
    if missing:
        print_error(f"Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    
    print_success("All dependencies installed!")
    return True

def test_env_file():
    """Test if .env file exists and has required keys"""
    print_section("TESTING ENVIRONMENT CONFIGURATION")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print_error(".env file not found!")
        print("Create .env from .env.example:")
        print("  cp .env.example .env")
        print("  Then edit .env with your API keys")
        return False
    
    print_success(".env file exists")
    
    # Check for ANTHROPIC_API_KEY
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if api_key and not api_key.startswith("sk-ant-"):
            print_warning("ANTHROPIC_API_KEY appears to be a placeholder")
            return False
        elif not api_key:
            print_error("ANTHROPIC_API_KEY not set in .env")
            return False
        
        print_success(f"ANTHROPIC_API_KEY configured (starts with {api_key[:10]}...)")
        
        # Check for optional keys
        voyage_key = os.getenv("VOYAGE_API_KEY", "")
        if voyage_key:
            print_success("VOYAGE_API_KEY configured (optional)")
        else:
            print_warning("VOYAGE_API_KEY not configured (using fallback search)")
        
        return True
        
    except Exception as e:
        print_error(f"Error reading .env: {e}")
        return False

def test_rag_system():
    """Test RAG implementation"""
    print_section("TESTING RAG SYSTEM")
    
    try:
        from app_implementation import ITSupportRAG
        
        print("Initializing RAG system...")
        rag = ITSupportRAG()
        
        print_success("RAG system initialized")
        print(f"  - Knowledge base size: {len(rag.knowledge_base)} characters")
        print(f"  - Embeddings enabled: {rag.use_embeddings}")
        print(f"  - Conversation history: {len(rag.conversation_history)} messages")
        
        # Test a sample query
        print("\nTesting keyword retrieval...")
        results = rag.retrieve_relevant_docs("WiFi connection")
        if results:
            print_success("Retrieved relevant documents")
            print(f"  - Retrieved {len(results.split(chr(10)))} lines")
        else:
            print_warning("No documents retrieved (empty knowledge base?)")
        
        return True
        
    except Exception as e:
        print_error(f"RAG system error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_server():
    """Test MCP server components"""
    print_section("TESTING MCP SERVER")
    
    try:
        from mcp_server import TicketManager
        
        print("Creating test ticket...")
        ticket = TicketManager.create_ticket(
            "Test issue: Cannot connect to WiFi",
            "High",
            "WiFi connection failing after update"
        )
        print_success(f"Created ticket: {ticket['ticket_id']}")
        
        print("Retrieving ticket status...")
        status = TicketManager.get_status_ticket(ticket['ticket_id'])
        print_success(f"Ticket status: {status['status']}")
        
        print("Listing all tickets...")
        all_tickets = TicketManager.list_tickets()
        print_success(f"Total tickets in system: {len(all_tickets)}")
        
        print("Updating ticket status...")
        updated = TicketManager.update_ticket_status(ticket['ticket_id'], 'IN_PROGRESS')
        print_success(f"Updated status: {updated['status']}")
        
        return True
        
    except Exception as e:
        print_error(f"MCP server error: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_next_steps():
    """Show next steps for running the application"""
    print_section("NEXT STEPS")
    
    print("""
1. RUN STREAMLIT WEB UI (Recommended):
   streamlit run streamlit.py
   
   Then open: http://localhost:8501
   
   Features:
   - Chat with the AI assistant
   - Create support tickets
   - Check ticket status
   - Search knowledge base

2. RUN CONSOLE CHATBOT:
   python3 app_implementation.py
   
   Commands:
   - Type questions to get IT support answers
   - "create ticket: <issue>" - Create a ticket
   - "check ticket: <id>" - Check ticket status
   - "quit" - Exit

3. RUN MCP SERVER:
   python3 mcp_server.py
   
   Then test endpoints:
   curl http://localhost:8000/health
   curl -X POST http://localhost:8000/mcp/create_ticket?issue=Test

4. RUN ALL COMPONENTS (3 terminals):
   Terminal 1: python3 mcp_server.py
   Terminal 2: streamlit run streamlit.py
   Terminal 3: (optional) tail -f logs if available

TROUBLESHOOTING:

• If you get "ModuleNotFoundError":
  pip install -r requirements.txt

• If you get "API key error":
  - Check .env file exists
  - Verify ANTHROPIC_API_KEY is set correctly
  - Get key from https://console.anthropic.com

• If Streamlit port is in use:
  streamlit run streamlit.py --server.port 8502

• If MCP server port is in use:
  Kill existing process: lsof -i :8000 && kill -9 <PID>

For more details, see README.md
""")

def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                 IT SUPPORT CHATBOT - TEST SUITE                      ║
║                      Ensuring Everything Works!                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    results = {
        "Dependencies": test_dependencies(),
        "Environment": test_env_file(),
        "RAG System": test_rag_system(),
        "MCP Server": test_mcp_server(),
    }
    
    # Summary
    print_section("TEST SUMMARY")
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print_success("All tests passed! Ready to run the application.")
        show_next_steps()
        return 0
    else:
        print_error("Some tests failed. Please fix the issues above.")
        print("\nFailed tests need to be resolved before running the app.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
