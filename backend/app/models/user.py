# User Model

from sqlalchemy import Column, String, Boolean, DateTime, UUID, func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime
import uuid

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    phone_number = Column(String(20))
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    
    # Email verification
    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True, index=True)
    is_superadmin = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    organization_members = relationship("OrganizationMember", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
