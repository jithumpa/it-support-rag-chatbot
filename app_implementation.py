"""
RAG Implementation for IT Support Chatbot
Uses VoyageAI embeddings and vector database for knowledge retrieval
"""

import os
from datetime import datetime
import json
from anthropic import Anthropic
from dotenv import load_dotenv
import requests

load_dotenv()

class ITSupportRAG:
    """IT Support Chatbot with RAG capabilities"""
    
    def __init__(self):
        """Initialize the RAG system"""
        self.client = Anthropic()
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []
        self.voyage_api_key = os.getenv("VOYAGE_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        # Initialize embeddings and vector DB if keys are available
        self.use_embeddings = bool(self.voyage_api_key and self.pinecone_api_key)
        
        if self.use_embeddings:
            print("✅ Using VoyageAI embeddings with Pinecone vector database")
            self._initialize_vector_db()
        else:
            print("⚠️ VoyageAI/Pinecone keys not found. Using fallback keyword matching.")
        
    def _initialize_vector_db(self):
        """Initialize vector database and load embeddings"""
        try:
            # Import Pinecone if available
            from pinecone import Pinecone
            
            self.pc = Pinecone(api_key=self.pinecone_api_key)
            self.index_name = os.getenv("PINECONE_INDEX_NAME", "it-support-kb")
            
            # Get index if it exists
            try:
                self.index = self.pc.Index(self.index_name)
                print(f"✅ Connected to Pinecone index: {self.index_name}")
                self._load_kb_to_pinecone()
            except Exception as e:
                print(f"⚠️ Could not connect to Pinecone index: {e}")
                self.use_embeddings = False
                
        except ImportError:
            print("⚠️ Pinecone not installed. Install with: pip install pinecone-client")
            self.use_embeddings = False
    
    def _load_kb_to_pinecone(self):
        """Load knowledge base chunks into Pinecone"""
        try:
            # Split knowledge base into chunks
            lines = self.knowledge_base.split('\n\n')  # Split by double newlines
            
            # Prepare vectors for upsert
            vectors = []
            for i, chunk in enumerate(lines):
                if chunk.strip():
                    # Get embedding from VoyageAI
                    embedding = self._get_embedding(chunk)
                    if embedding:
                        vectors.append({
                            "id": f"chunk_{i}",
                            "values": embedding,
                            "metadata": {"text": chunk[:500]}  # Store first 500 chars
                        })
            
            # Upsert vectors to Pinecone
            if vectors:
                self.index.upsert(vectors=vectors)
                print(f"✅ Loaded {len(vectors)} knowledge base chunks to Pinecone")
                
        except Exception as e:
            print(f"⚠️ Error loading KB to Pinecone: {e}")
    
    def _get_embedding(self, text: str) -> list:
        """Get embedding from VoyageAI API"""
        try:
            response = requests.post(
                "https://api.voyageai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.voyage_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": text,
                    "model": "voyage-2"
                }
            )
            
            if response.status_code == 200:
                return response.json()["data"][0]["embedding"]
            else:
                print(f"⚠️ VoyageAI API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error getting embedding: {e}")
            return None
        
    def _load_knowledge_base(self) -> str:
        """Load knowledge base from it_sector.txt"""
        try:
            with open("it_sector.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            print("Warning: it_sector.txt not found")
            return ""
    
    def get_current_datetime(self) -> str:
        """Tool: Get current date and time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def web_search(self, query: str) -> str:
        """Tool: Perform web search using knowledge base or external API"""
        # First try vector DB search
        if self.use_embeddings and hasattr(self, 'index'):
            try:
                query_embedding = self._get_embedding(query)
                if query_embedding:
                    results = self.index.query(
                        vector=query_embedding,
                        top_k=3,
                        include_metadata=True
                    )
                    
                    if results.get('matches'):
                        search_results = []
                        for match in results['matches']:
                            if 'metadata' in match and 'text' in match['metadata']:
                                search_results.append(match['metadata']['text'])
                        
                        return "\n".join(search_results) if search_results else f"Search results for: {query}"
            except Exception as e:
                print(f"Vector DB search failed: {e}")
        
        # Fallback: return generic result
        return f"Search results for: {query} (using local knowledge base)"
    
    def create_ticket(self, issue: str, priority: str = "Medium") -> dict:
        """MCP Tool: Create a support ticket"""
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "status": "success",
            "ticket_id": ticket_id,
            "issue": issue,
            "priority": priority,
            "created_at": self.get_current_datetime(),
            "status_code": "OPEN"
        }
    
    def get_status_ticket(self, ticket_id: str) -> dict:
        """MCP Tool: Get ticket status"""
        # In production, query actual ticket database
        return {
            "ticket_id": ticket_id,
            "status": "In Progress",
            "created_at": "2026-11-19 10:00:00",
            "last_updated": self.get_current_datetime(),
            "priority": "Medium"
        }
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant documents from knowledge base"""
        # Try vector DB search first
        if self.use_embeddings:
            try:
                query_embedding = self._get_embedding(query)
                if query_embedding and hasattr(self, 'index'):
                    results = self.index.query(
                        vector=query_embedding,
                        top_k=top_k,
                        include_metadata=True
                    )
                    
                    if results.get('matches'):
                        relevant_docs = []
                        for match in results['matches']:
                            if 'metadata' in match and 'text' in match['metadata']:
                                relevant_docs.append(match['metadata']['text'])
                        
                        if relevant_docs:
                            return '\n\n'.join(relevant_docs)
            except Exception as e:
                print(f"Vector search failed: {e}, falling back to keyword matching")
        
        # Fallback: Simple keyword matching
        lines = self.knowledge_base.split('\n')
        relevant_lines = []
        
        query_words = query.lower().split()
        for line in lines:
            if any(word in line.lower() for word in query_words):
                relevant_lines.append(line)
        
        return '\n'.join(relevant_lines[:top_k * 10])
    
    def chat(self, user_message: str) -> str:
        """Process user message and generate response using RAG"""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(user_message)
        
        # Build system prompt with RAG context
        system_prompt = f"""You are an IT Support Assistant. 
You have access to IT support knowledge base and can help users with technical issues.
You can also create and check support tickets.

KNOWLEDGE BASE:
{relevant_docs}

Current Date/Time: {self.get_current_datetime()}

When users report issues, be helpful and provide step-by-step solutions.
Offer to create a support ticket if the issue is complex."""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call Claude API with RAG context
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_tool_call(self, tool_name: str, **kwargs) -> str:
        """Process tool calls from MCP server"""
        if tool_name == "get_current_datetime":
            return self.get_current_datetime()
        elif tool_name == "web_search":
            return self.web_search(kwargs.get("query", ""))
        elif tool_name == "create_ticket":
            result = self.create_ticket(
                kwargs.get("issue", ""),
                kwargs.get("priority", "Medium")
            )
            return json.dumps(result)
        elif tool_name == "get_status_ticket":
            result = self.get_status_ticket(kwargs.get("ticket_id", ""))
            return json.dumps(result)
        else:
            return f"Unknown tool: {tool_name}"


def main():
    """Main function for testing RAG implementation"""
    rag_system = ITSupportRAG()
    
    print("=" * 60)
    print("IT Support Chatbot with RAG")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Chatbot: Thank you for using IT Support. Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Check for special commands
            if user_input.lower().startswith("create ticket:"):
                issue = user_input.replace("create ticket:", "").strip()
                ticket = rag_system.create_ticket(issue)
                print(f"Chatbot: Ticket created - ID: {ticket['ticket_id']}\n")
            
            elif user_input.lower().startswith("check ticket:"):
                ticket_id = user_input.replace("check ticket:", "").strip()
                ticket = rag_system.get_status_ticket(ticket_id)
                print(f"Chatbot: Ticket {ticket_id} Status: {ticket['status']}\n")
            
            else:
                # Regular chat with RAG
                response = rag_system.chat(user_message=user_input)
                print(f"Chatbot: {response}\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")


if __name__ == "__main__":
    main()
