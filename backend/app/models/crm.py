# CRM Models (Leads, Contacts, Deals, Companies)

from sqlalchemy import Column, String, Text, Integer, DateTime, UUID, ForeignKey, Numeric, Boolean, JSONB, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import LeadStatus

class Lead(BaseModel):
    __tablename__ = "crm_leads"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    # Lead Information
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), index=True)
    phone_number = Column(String(20))
    company = Column(String(255))
    job_title = Column(String(100))
    industry = Column(String(100))
    country = Column(String(100))
    
    # Lead Status
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    source = Column(String(50))  # phone_call, web_form, email, api, etc
    
    # Assignment
    assigned_to_user = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    assigned_at = Column(DateTime(timezone=True))
    
    # Pipeline
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("crm_pipelines.id"), nullable=True)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("crm_pipeline_stages.id"), nullable=True)
    
    # Value
    estimated_value = Column(Numeric(15, 2))
    currency = Column(String(3), default="USD")
    
    # Tracking
    last_contact_at = Column(DateTime(timezone=True))
    next_followup_at = Column(DateTime(timezone=True))
    contact_count = Column(Integer, default=0)
    
    # Additional Data
    custom_fields = Column(JSONB, default={})
    notes = Column(Text)
    tags = Column(JSONB, default=[])
    
    # Relationships
    organization = relationship("Organization", back_populates="leads")
    
    def __repr__(self):
        return f"<Lead {self.email}>"

class Contact(BaseModel):
    __tablename__ = "crm_contacts"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    email = Column(String(255), index=True)
    phone_number = Column(String(20), index=True)
    mobile_number = Column(String(20))
    company_id = Column(UUID(as_uuid=True), ForeignKey("crm_companies.id"), nullable=True)
    job_title = Column(String(100))
    department = Column(String(100))
    
    # Address
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    
    # Preferences
    preferred_communication = Column(String(50))  # email, phone, sms, whatsapp
    do_not_call = Column(Boolean, default=False)
    do_not_email = Column(Boolean, default=False)
    
    custom_fields = Column(JSONB, default={})
    notes = Column(Text)
    tags = Column(JSONB, default=[])
    
    def __repr__(self):
        return f"<Contact {self.email}>"

class Deal(BaseModel):
    __tablename__ = "crm_deals"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Amount & Value
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Pipeline & Status
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("crm_pipelines.id"), nullable=False)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("crm_pipeline_stages.id"), nullable=False)
    status = Column(String(50), default="open")  # open, won, lost
    
    # Timeline
    expected_close_date = Column(DateTime(timezone=True))
    actual_close_date = Column(DateTime(timezone=True))
    probability_percent = Column(Integer, default=50)
    
    # Relationships
    contact_id = Column(UUID(as_uuid=True), ForeignKey("crm_contacts.id"), nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("crm_companies.id"), nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    notes = Column(Text)
    tags = Column(JSONB, default=[])
    
    def __repr__(self):
        return f"<Deal {self.name}>"

class Company(BaseModel):
    __tablename__ = "crm_companies"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    website = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    employee_count = Column(Integer)
    annual_revenue = Column(Numeric(15, 2))
    
    custom_fields = Column(JSONB, default={})
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Company {self.name}>"

class Pipeline(BaseModel):
    __tablename__ = "crm_pipelines"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    
    stages = relationship("PipelineStage", back_populates="pipeline", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pipeline {self.name}>"

class PipelineStage(BaseModel):
    __tablename__ = "crm_pipeline_stages"
    
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("crm_pipelines.id"), nullable=False)
    name = Column(String(255), nullable=False)
    order_index = Column(Integer, nullable=False)
    color = Column(String(7))
    
    pipeline = relationship("Pipeline", back_populates="stages")
    
    def __repr__(self):
        return f"<PipelineStage {self.name}>"
