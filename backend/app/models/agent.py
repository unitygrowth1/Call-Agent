# Agent Model

from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, UUID, ForeignKey, JSONB, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import AgentType, AgentStatus

class Agent(BaseModel):
    __tablename__ = "agents"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(Text)
    agent_type = Column(Enum(AgentType), default=AgentType.GENERAL)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE, index=True)
    
    # Configuration
    personality = Column(Text)
    system_prompt = Column(Text)
    model_name = Column(String(100), default="llama2")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=500)
    voice_id = Column(String(100))
    language = Column(String(10), default="en")
    
    # Knowledge Base
    use_knowledge_base = Column(Boolean, default=False)
    knowledge_base_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id"), nullable=True)
    
    # Business Hours & Fallback
    enable_business_hours = Column(Boolean, default=False)
    business_hours = Column(JSONB, default={})
    fallback_type = Column(String(50))  # voicemail, transfer, schedule_callback
    fallback_target = Column(String(255))
    
    # Call Behavior
    enable_call_recording = Column(Boolean, default=True)
    enable_transcription = Column(Boolean, default=True)
    max_call_duration = Column(Integer, default=3600)
    end_call_phrase = Column(String(255))
    
    # Settings
    enable_context_retention = Column(Boolean, default=True)
    context_window = Column(Integer, default=10)
    enable_interruption_detection = Column(Boolean, default=True)
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="agents")
    workspace = relationship("Workspace", back_populates="agents")
    calls = relationship("Call", back_populates="agent")
    versions = relationship("AgentVersion", back_populates="agent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Agent {self.name}>"

class AgentVersion(BaseModel):
    __tablename__ = "agent_versions"
    
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    configuration = Column(JSONB, nullable=False)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    agent = relationship("Agent", back_populates="versions")
    
    def __repr__(self):
        return f"<AgentVersion {self.agent_id} v{self.version_number}>"
