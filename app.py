"""
Streamlit UI for IT Support Chatbot
Provides a web interface for the IT support chatbot with RAG capabilities
"""

import streamlit as st
import requests
import json
from datetime import datetime
from app_implementation import ITSupportRAG

# Page configuration
st.set_page_config(
    page_title="IT Support Chatbot",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .chat-user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .chat-bot {
        background-color: #f5f5f5;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "rag_system" not in st.session_state:
    st.session_state.rag_system = ITSupportRAG()
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# Sidebar
with st.sidebar:
    st.title("🛠️ IT Support Assistant")
    
    st.markdown("---")
    
    # Mode selection
    mode = st.radio(
        "Select Mode:",
        ["Chat", "Create Ticket", "Check Ticket", "Knowledge Base"]
    )
    
    st.markdown("---")
    
    # Settings
    st.subheader("Settings")
    temperature = st.slider("Response Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 256, 2048, 1024)
    
    st.markdown("---")
    
    # Statistics
    st.subheader("Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.conversation_history))
    with col2:
        st.metric("Tickets", len(st.session_state.tickets))
    
    st.markdown("---")
    
    # Clear history button
    if st.button("🔄 Clear Chat History", use_container_width=True):
        st.session_state.conversation_history = []
        st.rerun()


# Main content area
if mode == "Chat":
    st.title("💬 IT Support Chat")
    st.markdown("Ask me anything about IT support, common issues, and troubleshooting.")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.conversation_history):
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])
    
    # Input area
    st.markdown("---")
    user_input = st.chat_input("Ask me something...")
    
    if user_input:
        # Add user message to display
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response from RAG system
        with st.spinner("🔄 Generating response..."):
            response = st.session_state.rag_system.chat(user_input)
        
        # Add assistant response to history
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()


elif mode == "Create Ticket":
    st.title("🎫 Create Support Ticket")
    
    with st.form("ticket_form"):
        issue_title = st.text_input("Issue Title *", placeholder="e.g., Cannot connect to WiFi")
        
        issue_description = st.text_area(
            "Issue Description *",
            placeholder="Describe the issue in detail...",
            height=200
        )
        
        priority = st.selectbox(
            "Priority Level",
            ["Low", "Medium", "High", "Critical"]
        )
        
        category = st.selectbox(
            "Category",
            ["Network", "Email", "Printer", "Security", "Software", "Hardware", "Other"]
        )
        
        submitted = st.form_submit_button("📝 Create Ticket", use_container_width=True)
        
        if submitted and issue_title and issue_description:
            # Create ticket using RAG system
            ticket = st.session_state.rag_system.create_ticket(
                issue=issue_title,
                priority=priority
            )
            
            st.session_state.tickets.append(ticket)
            
            # Display success message
            st.success(f"✅ Ticket created successfully!")
            st.info(f"**Ticket ID:** {ticket['ticket_id']}")
            
            # Additional info
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Priority", ticket['priority'])
            with col2:
                st.metric("Status", ticket['status_code'])


elif mode == "Check Ticket":
    st.title("🔍 Check Ticket Status")
    
    ticket_id = st.text_input("Enter Ticket ID", placeholder="e.g., TKT-20261119101234")
    
    if ticket_id:
        ticket_status = st.session_state.rag_system.get_status_ticket(ticket_id)
        
        if ticket_status:
            st.success("Ticket found!")
            
            # Display ticket details
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ticket ID", ticket_status.get('ticket_id', 'N/A'))
                st.metric("Priority", ticket_status.get('priority', 'N/A'))
            
            with col2:
                st.metric("Status", ticket_status.get('status', 'N/A'))
                st.metric("Created", ticket_status.get('created_at', 'N/A'))
            
            # Additional details
            with st.expander("View Full Details"):
                st.json(ticket_status)
        else:
            st.warning("Ticket not found")


elif mode == "Knowledge Base":
    st.title("📚 Knowledge Base")
    
    # Load and display knowledge base
    rag_system = st.session_state.rag_system
    knowledge_base = rag_system.knowledge_base
    
    if knowledge_base:
        # Search knowledge base
        search_term = st.text_input("Search knowledge base", placeholder="e.g., network, wifi, email")
        
        if search_term:
            # Find relevant sections
            results = rag_system.retrieve_relevant_docs(search_term, top_k=5)
            
            if results:
                st.markdown("### Search Results")
                st.markdown(results)
            else:
                st.info("No results found for your search")
        
        else:
            # Display full knowledge base
            st.markdown("### Full Knowledge Base")
            with st.expander("View Knowledge Base Content"):
                st.text(knowledge_base)
    else:
        st.warning("Knowledge base not loaded")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        IT Support Chatbot | Powered by Claude AI | RAG with VoyageAI Embeddings
    </div>
    """,
    unsafe_allow_html=True
)
