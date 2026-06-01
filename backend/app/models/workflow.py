# Workflow & Automation Models

from sqlalchemy import Column, String, Text, Integer, DateTime, UUID, ForeignKey, JSONB, Enum, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import WorkflowStatus, TriggerType

class Workflow(BaseModel):
    __tablename__ = "workflows"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT, index=True)
    
    # Trigger
    trigger_type = Column(Enum(TriggerType), nullable=False)
    trigger_config = Column(JSONB, nullable=False)
    
    # Workflow Definition
    nodes = Column(JSONB, nullable=False)  # Workflow steps
    edges = Column(JSONB, nullable=False)  # Connections between steps
    
    # Settings
    run_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    last_run_at = Column(DateTime(timezone=True))
    
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    organization = relationship("Organization", back_populates="workflows")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow {self.name}>"

class WorkflowExecution(BaseModel):
    __tablename__ = "workflow_executions"
    
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    status = Column(String(50), default="pending", index=True)  # pending, running, success, failed
    trigger_data = Column(JSONB, nullable=False)
    execution_log = Column(JSONB, default=[])
    error_message = Column(Text)
    
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow())
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Integer)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="executions")
    
    def __repr__(self):
        return f"<WorkflowExecution {self.workflow_id}>"

from datetime import datetime
