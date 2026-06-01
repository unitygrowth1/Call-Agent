# Call Model

from sqlalchemy import Column, String, Integer, DateTime, UUID, ForeignKey, Text, Boolean, Float, JSONB, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import CallType, CallStatus

class Call(BaseModel):
    __tablename__ = "calls"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    
    # Call Details
    call_type = Column(Enum(CallType), nullable=False)
    status = Column(Enum(CallStatus), default=CallStatus.INITIATED, index=True)
    direction = Column(String(50))
    
    # Participants
    from_number = Column(String(20), nullable=False)
    to_number = Column(String(20), nullable=False)
    caller_id = Column(String(255))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("crm_contacts.id"), nullable=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("crm_leads.id"), nullable=True)
    
    # Duration
    started_at = Column(DateTime(timezone=True))
    answered_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer, default=0)
    wait_time_seconds = Column(Integer, default=0)
    
    # Recording & Transcription
    recording_url = Column(String(500))
    transcript = Column(Text)
    transcript_segments = Column(JSONB)
    
    # AI Interaction
    ai_processed = Column(Boolean, default=False)
    ai_summary = Column(Text)
    ai_sentiment = Column(String(50))
    ai_intent = Column(String(100))
    
    # Quality & Notes
    call_quality = Column(String(50))
    notes = Column(Text)
    tags = Column(JSONB, default=[])
    
    # Metadata
    call_sid = Column(String(255))
    metadata = Column(JSONB, default={})
    
    # Relationships
    organization = relationship("Organization", back_populates="calls")
    agent = relationship("Agent", back_populates="calls")
    transcripts = relationship("CallTranscript", back_populates="call", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Call {self.id}>"

class CallTranscript(BaseModel):
    __tablename__ = "call_transcripts"
    
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    speaker = Column(String(50))  # user, agent, system
    message = Column(Text, nullable=False)
    timestamp = Column(Integer)  # milliseconds into call
    confidence = Column(Float)
    
    # Relationships
    call = relationship("Call", back_populates="transcripts")
    
    def __repr__(self):
        return f"<CallTranscript {self.call_id}>"
