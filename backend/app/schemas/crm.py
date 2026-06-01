# CRM Schemas

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid
from app.core.constants import LeadStatus

class LeadCreateRequest(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    source: str = "phone_call"
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "+1-555-0100",
                "company": "Acme Corp",
                "job_title": "CEO",
                "industry": "Technology",
                "source": "phone_call",
                "notes": "Interested in demo"
            }
        }

class LeadUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[LeadStatus] = None
    assigned_to_user: Optional[uuid.UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    estimated_value: Optional[float] = None

class LeadResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    company: Optional[str]
    status: LeadStatus
    source: str
    contact_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LeadDetailResponse(LeadResponse):
    job_title: Optional[str]
    industry: Optional[str]
    assigned_to_user: Optional[uuid.UUID]
    estimated_value: Optional[float]
    last_contact_at: Optional[datetime]
    next_followup_at: Optional[datetime]
    notes: Optional[str]
    tags: List[str]

class ContactResponse(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    job_title: Optional[str]
    department: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DealResponse(BaseModel):
    id: uuid.UUID
    name: str
    amount: float
    status: str
    stage_id: Optional[uuid.UUID]
    contact_id: Optional[uuid.UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True
