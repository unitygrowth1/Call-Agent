# Organization & Workspace Models

from sqlalchemy import Column, String, Text, Boolean, DateTime, UUID, ForeignKey, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"
    
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(255))
    timezone = Column(String(50), default="UTC")
    country = Column(String(100))
    industry = Column(String(100))
    company_size = Column(String(50))
    plan_type = Column(String(50), default="free")
    status = Column(String(50), default="active", index=True)
    
    # Relationships
    workspaces = relationship("Workspace", back_populates="organization", cascade="all, delete-orphan")
    members = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="organization", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="organization", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="organization", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="organization", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="organization", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="organization", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Organization {self.name}>"

class Workspace(BaseModel):
    __tablename__ = "workspaces"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    status = Column(String(50), default="active")
    
    # Relationships
    organization = relationship("Organization", back_populates="workspaces")
    agents = relationship("Agent", back_populates="workspace", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workspace {self.name}>"

class OrganizationMember(BaseModel):
    __tablename__ = "organization_members"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=True)
    role = Column(String(50), default="user")  # owner, admin, user, guest
    permissions = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    invited_at = Column(DateTime(timezone=True), nullable=True)
    joined_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organization_members")
    
    def __repr__(self):
        return f"<OrganizationMember {self.user_id}@{self.organization_id}>"
