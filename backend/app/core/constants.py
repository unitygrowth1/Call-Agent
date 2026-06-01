# Constants

from enum import Enum

# User Roles
class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# Agent Types
class AgentType(str, Enum):
    GENERAL = "general"
    SALES = "sales"
    SUPPORT = "support"
    RECEPTIONIST = "receptionist"

# Agent Status
class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

# Call Types
class CallType(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

# Call Status
class CallStatus(str, Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    CONNECTED = "connected"
    COMPLETED = "completed"
    FAILED = "failed"
    MISSED = "missed"

# Lead Status
class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    WON = "won"
    LOST = "lost"

# Workflow Status
class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

# Trigger Types
class TriggerType(str, Enum):
    NEW_LEAD = "new_lead"
    CALL_COMPLETED = "call_completed"
    FORM_SUBMITTED = "form_submitted"
    MISSED_CALL = "missed_call"
    APPOINTMENT_BOOKED = "appointment_booked"
    PAYMENT_RECEIVED = "payment_received"

# Communication Channels
class CommunicationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    VOICE = "voice"

# Permission Levels
PERMISSIONS = {
    "agents": ["create", "read", "update", "delete"],
    "calls": ["read", "record", "transfer"],
    "crm": ["create", "read", "update", "delete"],
    "workflows": ["create", "read", "update", "delete", "execute"],
    "users": ["invite", "manage"],
    "settings": ["read", "update"],
}

# Default permissions by role
ROLE_PERMISSIONS = {
    UserRole.OWNER: {
        "agents": ["create", "read", "update", "delete"],
        "calls": ["read", "record", "transfer"],
        "crm": ["create", "read", "update", "delete"],
        "workflows": ["create", "read", "update", "delete", "execute"],
        "users": ["invite", "manage"],
        "settings": ["read", "update"],
    },
    UserRole.ADMIN: {
        "agents": ["create", "read", "update", "delete"],
        "calls": ["read", "record", "transfer"],
        "crm": ["create", "read", "update", "delete"],
        "workflows": ["create", "read", "update", "delete", "execute"],
        "users": ["invite"],
        "settings": ["read"],
    },
    UserRole.USER: {
        "agents": ["read"],
        "calls": ["read"],
        "crm": ["create", "read", "update"],
        "workflows": ["read", "execute"],
        "users": [],
        "settings": ["read"],
    },
    UserRole.GUEST: {
        "agents": ["read"],
        "calls": ["read"],
        "crm": ["read"],
        "workflows": ["read"],
        "users": [],
        "settings": [],
    },
}
