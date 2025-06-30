"""
Maestro Builder API
A FastAPI application to support the Maestro Builder frontend application.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import yaml
from datetime import datetime
import uuid
import os
from pathlib import Path

# Import our AI agent
from ai_agent import MaestroBuilderAgent

# Initialize FastAPI app
app = FastAPI(
    title="Maestro Builder API",
    description="API for the Maestro Builder application",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI agent
ai_agent = MaestroBuilderAgent()

# Data models
class ChatMessage(BaseModel):
    content: str
    role: str = "user"

class ChatResponse(BaseModel):
    response: str
    yaml_files: List[Dict[str, str]]

class ChatHistory(BaseModel):
    id: str
    name: str
    created_at: datetime
    last_message: str
    message_count: int

class YamlFile(BaseModel):
    name: str
    content: str

# In-memory storage for chat sessions and history
# In a production environment, this would be replaced with a database
chat_sessions: Dict[str, Dict[str, Any]] = {}
chat_history: List[Dict[str, Any]] = []

# Initialize storage directory
STORAGE_DIR = Path(__file__).parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

def save_chat_session(chat_id: str, session_data: Dict[str, Any]):
    """Save chat session to file"""
    session_file = STORAGE_DIR / f"chat_{chat_id}.json"
    with open(session_file, 'w') as f:
        json.dump(session_data, f, default=str)

def load_chat_session(chat_id: str) -> Optional[Dict[str, Any]]:
    """Load chat session from file"""
    session_file = STORAGE_DIR / f"chat_{chat_id}.json"
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f)
    return None

def save_chat_history():
    """Save chat history to file"""
    history_file = STORAGE_DIR / "chat_history.json"
    with open(history_file, 'w') as f:
        json.dump(chat_history, f, default=str)

def load_chat_history():
    """Load chat history from file"""
    history_file = STORAGE_DIR / "chat_history.json"
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

# Load existing chat history on startup
chat_history = load_chat_history()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Maestro Builder API", "version": "1.0.0"}

@app.post("/api/chat_builder_agent", response_model=ChatResponse)
async def chat_builder_agent(message: ChatMessage, chat_id: Optional[str] = None):
    """
    Chat with the Maestro Builder agent to create YAML configurations.
    
    Args:
        message: The chat message from the user
        chat_id: Optional chat session ID for continuing conversations
    
    Returns:
        ChatResponse with AI response and updated YAML files
    """
    try:
        # Generate or use existing chat ID
        if not chat_id:
            chat_id = str(uuid.uuid4())
        
        # Load existing session or create new one
        session = load_chat_session(chat_id) or {
            "id": chat_id,
            "messages": [],
            "yaml_files": {
                "agents.yaml": "# Agents configuration will be generated here\nagents:\n  # Your agents will appear here",
                "workflow.yaml": "# Workflow configuration will be generated here\nworkflow:\n  # Your workflow will appear here"
            },
            "created_at": datetime.now().isoformat()
        }
        
        # Add user message to session
        session["messages"].append({
            "role": "user",
            "content": message.content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate AI response using the MaestroBuilderAgent
        ai_response = ai_agent.generate_response(message.content, session["yaml_files"])
        
        # Add AI response to session
        session["messages"].append({
            "role": "assistant",
            "content": ai_response["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Update YAML files
        session["yaml_files"] = ai_response["yaml_files"]
        
        # Save session
        save_chat_session(chat_id, session)
        
        # Update chat history
        update_chat_history(chat_id, message.content)
        
        return ChatResponse(
            response=ai_response["response"],
            yaml_files=[{"name": name, "content": content} for name, content in session["yaml_files"].items()]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/api/get_yamls/{chat_id}", response_model=List[YamlFile])
async def get_yamls(chat_id: str):
    """
    Get the YAML files for a specific chat session.
    
    Args:
        chat_id: The chat session ID
    
    Returns:
        List of YAML files with their content
    """
    try:
        session = load_chat_session(chat_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        yaml_files = []
        for name, content in session["yaml_files"].items():
            yaml_files.append(YamlFile(name=name, content=content))
        
        return yaml_files
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving YAML files: {str(e)}")

@app.get("/api/chat_history", response_model=List[ChatHistory])
async def get_chat_history():
    """
    Get the history of all chat conversations.
    
    Returns:
        List of chat history entries
    """
    try:
        history = []
        for chat in chat_history:
            history.append(ChatHistory(
                id=chat["id"],
                name=chat["name"],
                created_at=datetime.fromisoformat(chat["created_at"]),
                last_message=chat["last_message"],
                message_count=chat["message_count"]
            ))
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

def update_chat_history(chat_id: str, last_message: str):
    """Update chat history with new message"""
    # Check if chat already exists in history
    existing_chat = None
    for chat in chat_history:
        if chat["id"] == chat_id:
            existing_chat = chat
            break
    
    if existing_chat:
        # Update existing chat
        existing_chat["last_message"] = last_message
        existing_chat["message_count"] += 1
    else:
        # Create new chat entry
        chat_history.append({
            "id": chat_id,
            "name": f"Chat {len(chat_history) + 1}",
            "created_at": datetime.now().isoformat(),
            "last_message": last_message,
            "message_count": 1
        })
    
    # Save updated history
    save_chat_history()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 