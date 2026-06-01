# Call Schemas

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from app.core.constants import CallType, CallStatus

class CallCreateRequest(BaseModel):
    call_type: CallType
    from_number: str
    to_number: str
    agent_id: Optional[uuid.UUID] = None
    customer_id: Optional[uuid.UUID] = None
    lead_id: Optional[uuid.UUID] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "call_type": "outbound",
                "from_number": "+1-555-0100",
                "to_number": "+1-555-0101",
                "agent_id": "uuid-here",
            }
        }

class CallUpdateRequest(BaseModel):
    status: Optional[CallStatus] = None
    notes: Optional[str] = None
    call_quality: Optional[str] = None
    ai_sentiment: Optional[str] = None
    ai_intent: Optional[str] = None
    tags: Optional[List[str]] = None

class CallResponse(BaseModel):
    id: uuid.UUID
    call_type: CallType
    status: CallStatus
    from_number: str
    to_number: str
    duration_seconds: int
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    recording_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CallDetailResponse(CallResponse):
    agent_id: Optional[uuid.UUID]
    customer_id: Optional[uuid.UUID]
    lead_id: Optional[uuid.UUID]
    transcript: Optional[str]
    ai_summary: Optional[str]
    ai_sentiment: Optional[str]
    ai_intent: Optional[str]
    call_quality: Optional[str]
    notes: Optional[str]
    tags: List[str]

class CallTranscriptResponse(BaseModel):
    id: uuid.UUID
    speaker: str
    message: str
    timestamp: Optional[int]
    confidence: Optional[float]
    
    class Config:
        from_attributes = True
