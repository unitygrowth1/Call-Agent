# Agent Schemas

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from app.core.constants import AgentType, AgentStatus

class AgentCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    agent_type: AgentType = AgentType.GENERAL
    personality: Optional[str] = None
    system_prompt: Optional[str] = None
    model_name: str = "llama2"
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(500, ge=1, le=4000)
    voice_id: Optional[str] = None
    language: str = "en"
    use_knowledge_base: bool = False
    knowledge_base_id: Optional[uuid.UUID] = None
    enable_call_recording: bool = True
    enable_transcription: bool = True
    max_call_duration: int = 3600
    enable_context_retention: bool = True
    context_window: int = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sales Assistant",
                "description": "AI agent for handling sales calls",
                "agent_type": "sales",
                "personality": "Professional, friendly, and knowledgeable",
                "system_prompt": "You are a helpful sales assistant...",
                "model_name": "llama2",
                "temperature": 0.7,
                "max_tokens": 500,
                "voice_id": "en_US_1",
                "language": "en"
            }
        }

class AgentUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None
    system_prompt: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4000)
    voice_id: Optional[str] = None
    language: Optional[str] = None
    status: Optional[AgentStatus] = None
    use_knowledge_base: Optional[bool] = None
    knowledge_base_id: Optional[uuid.UUID] = None

class AgentResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: Optional[str]
    agent_type: AgentType
    status: AgentStatus
    model_name: str
    voice_id: Optional[str]
    language: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AgentDetailResponse(AgentResponse):
    personality: Optional[str]
    system_prompt: Optional[str]
    temperature: float
    max_tokens: int
    use_knowledge_base: bool
    knowledge_base_id: Optional[uuid.UUID]
    enable_call_recording: bool
    enable_transcription: bool
    max_call_duration: int
    enable_context_retention: bool
    context_window: int
