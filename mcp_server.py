"""
MCP Server for IT Support Chatbot
Provides ticket management services: create_ticket and get_status_ticket
"""

import os
import json
from datetime import datetime
from typing import Any
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# In-memory ticket storage (in production, use a database)
tickets_database = {}

class TicketManager:
    """Manages support tickets"""
    
    @staticmethod
    def create_ticket(issue: str, priority: str = "Medium", description: str = "") -> dict:
        """
        Create a new support ticket
        
        Args:
            issue: Brief description of the issue
            priority: Ticket priority (Low, Medium, High, Critical)
            description: Detailed description
            
        Returns:
            Ticket object with ID and details
        """
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        ticket = {
            "ticket_id": ticket_id,
            "issue": issue,
            "description": description or issue,
            "priority": priority,
            "status": "OPEN",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "assignee": None,
            "resolution": None,
            "resolution_date": None
        }
        
        tickets_database[ticket_id] = ticket
        return ticket
    
    @staticmethod
    def get_status_ticket(ticket_id: str) -> dict:
        """
        Get the status of a support ticket
        
        Args:
            ticket_id: The ticket ID to check
            
        Returns:
            Ticket details with current status
        """
        if ticket_id in tickets_database:
            return tickets_database[ticket_id]
        else:
            return {
                "error": f"Ticket {ticket_id} not found",
                "ticket_id": ticket_id,
                "status": "NOT_FOUND"
            }
    
    @staticmethod
    def update_ticket_status(ticket_id: str, status: str) -> dict:
        """Update ticket status"""
        if ticket_id in tickets_database:
            tickets_database[ticket_id]["status"] = status
            tickets_database[ticket_id]["last_updated"] = datetime.now().isoformat()
            return tickets_database[ticket_id]
        return {"error": f"Ticket {ticket_id} not found"}
    
    @staticmethod
    def list_tickets(status: str = None) -> list:
        """List all tickets, optionally filtered by status"""
        if status:
            return [t for t in tickets_database.values() if t["status"] == status]
        return list(tickets_database.values())


# FastAPI Routes

@app.post("/mcp/create_ticket")
def create_ticket_endpoint(issue: str, priority: str = "Medium", description: str = ""):
    """MCP Endpoint: Create a support ticket"""
    try:
        ticket = TicketManager.create_ticket(issue, priority, description)
        return {
            "status": "success",
            "data": ticket
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/mcp/get_status_ticket/{ticket_id}")
def get_status_ticket_endpoint(ticket_id: str):
    """MCP Endpoint: Get ticket status"""
    try:
        ticket = TicketManager.get_status_ticket(ticket_id)
        if "error" in ticket:
            return {
                "status": "not_found",
                "data": ticket
            }
        return {
            "status": "success",
            "data": ticket
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.put("/mcp/update_ticket/{ticket_id}")
def update_ticket_endpoint(ticket_id: str, status: str):
    """Update ticket status"""
    try:
        ticket = TicketManager.update_ticket_status(ticket_id, status)
        if "error" in ticket:
            return {
                "status": "not_found",
                "data": ticket
            }
        return {
            "status": "success",
            "data": ticket
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/mcp/list_tickets")
def list_tickets_endpoint(status: str = None):
    """List all tickets"""
    try:
        tickets = TicketManager.list_tickets(status)
        return {
            "status": "success",
            "count": len(tickets),
            "data": tickets
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "IT Support MCP Server",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "IT Support Chatbot - MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "create_ticket": "POST /mcp/create_ticket",
            "get_status_ticket": "GET /mcp/get_status_ticket/{ticket_id}",
            "update_ticket": "PUT /mcp/update_ticket/{ticket_id}",
            "list_tickets": "GET /mcp/list_tickets",
            "health": "GET /health"
        }
    }


def main():
    """Run the MCP server"""
    print("=" * 60)
    print("IT Support MCP Server")
    print("=" * 60)
    print("Starting server on http://0.0.0.0:8000")
    print("\nAvailable endpoints:")
    print("  - POST   /mcp/create_ticket")
    print("  - GET    /mcp/get_status_ticket/{ticket_id}")
    print("  - PUT    /mcp/update_ticket/{ticket_id}")
    print("  - GET    /mcp/list_tickets")
    print("  - GET    /health")
    print("\nPress Ctrl+C to stop server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
