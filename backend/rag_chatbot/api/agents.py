from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai.agent_manager import AgentManager
from ai.agent_tools import AgentTools


router = APIRouter()


# Request/Response models
class AgentCreateRequest(BaseModel):
    name: str
    instructions: Optional[str] = "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Use the provided tools to answer questions accurately and comprehensively."
    model: Optional[str] = None  # Will use default from settings if not provided


class AgentCreateResponse(BaseModel):
    agent_id: str
    name: str
    status: str


class AgentQueryRequest(BaseModel):
    query: str
    agent_id: Optional[str] = None  # If not provided, will use default agent
    conversation_history: Optional[List[Dict[str, str]]] = []
    selected_text: Optional[str] = None  # For selected text queries
    tools_enabled: Optional[bool] = True


class AgentQueryResponse(BaseModel):
    response: str
    agent_id: str
    sources: List[Dict[str, Any]]
    tool_calls: Optional[List[Dict[str, Any]]] = []
    status: str


class AgentListResponse(BaseModel):
    agents: List[Dict[str, Any]]
    total: int


@router.post("/create", response_model=AgentCreateResponse)
async def create_agent(request: AgentCreateRequest):
    """Create a new AI agent with specified parameters"""
    try:
        # In a real implementation, you would store agent configuration
        # For now, we'll just return a success response
        return AgentCreateResponse(
            agent_id="default_agent",  # Using default agent for now
            name=request.name,
            status="created"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")


@router.post("/query", response_model=AgentQueryResponse)
async def query_agent(request: AgentQueryRequest):
    """Query an AI agent with the provided query and context"""
    try:
        agent_manager = AgentManager()

        result = agent_manager.generate_response(
            user_query=request.query,
            conversation_history=request.conversation_history,
            selected_text=request.selected_text
        )

        return AgentQueryResponse(
            response=result.get("response", ""),
            agent_id=result.get("thread_id", "default_agent"),
            sources=result.get("sources", []),
            tool_calls=result.get("tool_calls", []),
            status=result.get("status", "success")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying agent: {str(e)}")


@router.post("/query_with_selection", response_model=AgentQueryResponse)
async def query_agent_with_selection(request: AgentQueryRequest):
    """Query an AI agent with selected text context"""
    try:
        agent_manager = AgentManager()

        # Combine the query with selected text context
        if request.selected_text:
            full_query = f"Regarding the selected text: '{request.selected_text}', {request.query}"
        else:
            full_query = request.query

        result = agent_manager.generate_response(
            user_query=full_query,
            conversation_history=request.conversation_history,
            selected_text=request.selected_text
        )

        return AgentQueryResponse(
            response=result.get("response", ""),
            agent_id=result.get("thread_id", "default_agent"),
            sources=result.get("sources", []),
            tool_calls=result.get("tool_calls", []),
            status=result.get("status", "success")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying agent with selection: {str(e)}")


@router.get("/list", response_model=AgentListResponse)
async def list_agents():
    """List available AI agents"""
    try:
        # In a real implementation, you would return stored agents
        # For now, return a default agent
        agents = [{
            "id": "default_agent",
            "name": "Physical AI Textbook Assistant",
            "description": "AI assistant for the Physical AI & Humanoid Robotics textbook",
            "capabilities": ["textbook_search", "content_explanation", "glossary_lookup", "chapter_outlines"],
            "status": "active"
        }]

        return AgentListResponse(
            agents=agents,
            total=len(agents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing agents: {str(e)}")


@router.get("/tools")
async def list_agent_tools():
    """List available tools for AI agents"""
    try:
        tools_manager = AgentTools()
        tools = tools_manager.get_all_tools()

        return {"tools": tools, "count": len(tools)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")


@router.post("/execute_tool")
async def execute_agent_tool(tool_name: str, arguments: Dict[str, Any]):
    """Execute a specific agent tool with provided arguments"""
    try:
        tools_manager = AgentTools()

        # Dispatch to the appropriate tool method
        if tool_name == "search_textbook_content":
            result = tools_manager.search_textbook_content(**arguments)
        elif tool_name == "get_chapter_outline":
            result = tools_manager.get_chapter_outline(**arguments)
        elif tool_name == "get_glossary_terms":
            result = tools_manager.get_glossary_terms(**arguments)
        elif tool_name == "get_related_concepts":
            result = tools_manager.get_related_concepts(**arguments)
        elif tool_name == "explain_application":
            result = tools_manager.explain_application(**arguments)
        else:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")