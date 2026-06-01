# Call Agent - Database Schema

## Overview

The database uses PostgreSQL with SQLAlchemy ORM. Multi-tenancy is implemented through row-level security (RLS) with `organization_id` on every table.

## Core Tables

### Users & Organizations

#### organizations (Tenants)
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    website VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'UTC',
    country VARCHAR(100),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    plan_type VARCHAR(50) DEFAULT 'free', -- free, starter, pro, enterprise
    status VARCHAR(50) DEFAULT 'active', -- active, suspended, deleted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organizations_status ON organizations(status);
```

#### workspaces
```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, slug)
);
CREATE INDEX idx_workspaces_org_id ON workspaces(organization_id);
```

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    phone_number VARCHAR(20),
    timezone VARCHAR(50) DEFAULT 'UTC',
    language VARCHAR(10) DEFAULT 'en',
    is_email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_superadmin BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
```

#### organization_members (Team Members)
```sql
CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id) ON DELETE SET NULL,
    role VARCHAR(50) DEFAULT 'user', -- owner, admin, user, guest
    permissions JSONB DEFAULT '{}', -- Custom permissions
    is_active BOOLEAN DEFAULT TRUE,
    invited_at TIMESTAMP,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, user_id)
);
CREATE INDEX idx_org_members_org_user ON organization_members(organization_id, user_id);
CREATE INDEX idx_org_members_role ON organization_members(role);
```

### Agents

#### agents
```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    agent_type VARCHAR(50) DEFAULT 'general', -- general, sales, support, receptionist
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, archived
    
    -- Agent Configuration
    personality TEXT, -- Agent personality/instructions
    system_prompt TEXT, -- System prompt for LLM
    model_name VARCHAR(100) DEFAULT 'llama2', -- llama2, qwen, mistral, etc
    temperature FLOAT DEFAULT 0.7,
    max_tokens INT DEFAULT 500,
    voice_id VARCHAR(100), -- Voice selection
    language VARCHAR(10) DEFAULT 'en',
    
    -- Knowledge Base
    use_knowledge_base BOOLEAN DEFAULT FALSE,
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE SET NULL,
    
    -- Business Hours & Fallback
    enable_business_hours BOOLEAN DEFAULT FALSE,
    business_hours JSONB DEFAULT '{}', -- {"monday": {"start": "09:00", "end": "17:00"}, ...}
    fallback_type VARCHAR(50), -- voicemail, transfer, schedule_callback
    fallback_target VARCHAR(255), -- Phone number or email for fallback
    
    -- Call Behavior
    enable_call_recording BOOLEAN DEFAULT TRUE,
    enable_transcription BOOLEAN DEFAULT TRUE,
    max_call_duration INT DEFAULT 3600, -- seconds
    end_call_phrase VARCHAR(255),
    
    -- Settings
    enable_context_retention BOOLEAN DEFAULT TRUE,
    context_window INT DEFAULT 10, -- Number of previous messages to keep
    enable_interruption_detection BOOLEAN DEFAULT TRUE,
    
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    
    UNIQUE(workspace_id, slug)
);
CREATE INDEX idx_agents_org_workspace ON agents(organization_id, workspace_id);
CREATE INDEX idx_agents_status ON agents(status);
```

#### agent_versions (Version control for agents)
```sql
CREATE TABLE agent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    configuration JSONB NOT NULL, -- Full agent config snapshot
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_id, version_number)
);
CREATE INDEX idx_agent_versions_agent_id ON agent_versions(agent_id);
```

### Calls & Communication

#### calls
```sql
CREATE TABLE calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    
    -- Call Details
    call_type VARCHAR(50) NOT NULL, -- inbound, outbound
    status VARCHAR(50) DEFAULT 'initiated', -- initiated, ringing, connected, completed, failed
    direction VARCHAR(50), -- inbound, outbound
    
    -- Participants
    from_number VARCHAR(20) NOT NULL,
    to_number VARCHAR(20) NOT NULL,
    caller_id VARCHAR(255),
    customer_id UUID REFERENCES crm_contacts(id) ON DELETE SET NULL,
    lead_id UUID REFERENCES crm_leads(id) ON DELETE SET NULL,
    
    -- Duration
    started_at TIMESTAMP,
    answered_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INT DEFAULT 0,
    wait_time_seconds INT DEFAULT 0,
    
    -- Recording & Transcription
    recording_url VARCHAR(500),
    transcript TEXT,
    transcript_segments JSONB, -- Detailed conversation segments
    
    -- AI Interaction
    ai_processed BOOLEAN DEFAULT FALSE,
    ai_summary TEXT,
    ai_sentiment VARCHAR(50), -- positive, neutral, negative
    ai_intent VARCHAR(100),
    
    -- Quality & Notes
    call_quality VARCHAR(50), -- excellent, good, fair, poor
    notes TEXT,
    tags JSONB DEFAULT '[]',
    
    -- Metadata
    call_sid VARCHAR(255), -- External call ID (Twilio, etc)
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_calls_org_workspace ON calls(organization_id, workspace_id);
CREATE INDEX idx_calls_agent_id ON calls(agent_id);
CREATE INDEX idx_calls_status ON calls(status);
CREATE INDEX idx_calls_direction ON calls(direction);
CREATE INDEX idx_calls_created_at ON calls(created_at);
```

#### call_transcripts (Detailed call data)
```sql
CREATE TABLE call_transcripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_id UUID NOT NULL REFERENCES calls(id) ON DELETE CASCADE,
    speaker VARCHAR(50), -- user, agent, system
    message TEXT NOT NULL,
    timestamp INT, -- milliseconds into call
    confidence FLOAT, -- STT confidence
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_transcripts_call_id ON call_transcripts(call_id);
```

### CRM

#### crm_leads
```sql
CREATE TABLE crm_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Lead Information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    company VARCHAR(255),
    job_title VARCHAR(100),
    industry VARCHAR(100),
    country VARCHAR(100),
    
    -- Lead Status
    status VARCHAR(50) DEFAULT 'new', -- new, contacted, qualified, proposal_sent, won, lost
    source VARCHAR(50), -- phone_call, web_form, email, api, etc
    
    -- Assignment
    assigned_to_user UUID REFERENCES users(id) ON DELETE SET NULL,
    assigned_at TIMESTAMP,
    
    -- Pipeline
    pipeline_id UUID REFERENCES crm_pipelines(id) ON DELETE SET NULL,
    stage_id UUID REFERENCES crm_pipeline_stages(id) ON DELETE SET NULL,
    
    -- Value
    estimated_value DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Tracking
    last_contact_at TIMESTAMP,
    next_followup_at TIMESTAMP,
    contact_count INT DEFAULT 0,
    
    -- Additional Data
    custom_fields JSONB DEFAULT '{}',
    notes TEXT,
    tags JSONB DEFAULT '[]',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_leads_org_workspace ON crm_leads(organization_id, workspace_id);
CREATE INDEX idx_leads_status ON crm_leads(status);
CREATE INDEX idx_leads_assigned_to ON crm_leads(assigned_to_user);
CREATE INDEX idx_leads_email ON crm_leads(email);
```

#### crm_contacts
```sql
CREATE TABLE crm_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    mobile_number VARCHAR(20),
    company_id UUID REFERENCES crm_companies(id) ON DELETE SET NULL,
    job_title VARCHAR(100),
    department VARCHAR(100),
    
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    
    preferred_communication VARCHAR(50), -- email, phone, sms, whatsapp
    do_not_call BOOLEAN DEFAULT FALSE,
    do_not_email BOOLEAN DEFAULT FALSE,
    
    custom_fields JSONB DEFAULT '{}',
    notes TEXT,
    tags JSONB DEFAULT '[]',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_contacts_org_workspace ON crm_contacts(organization_id, workspace_id);
CREATE INDEX idx_contacts_email ON crm_contacts(email);
CREATE INDEX idx_contacts_phone ON crm_contacts(phone_number);
```

#### crm_deals
```sql
CREATE TABLE crm_deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Amount & Value
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Pipeline & Status
    pipeline_id UUID NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
    stage_id UUID NOT NULL REFERENCES crm_pipeline_stages(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'open', -- open, won, lost
    
    -- Timeline
    expected_close_date DATE,
    actual_close_date DATE,
    probability_percent INT DEFAULT 50,
    
    -- Relationships
    contact_id UUID REFERENCES crm_contacts(id) ON DELETE SET NULL,
    company_id UUID REFERENCES crm_companies(id) ON DELETE SET NULL,
    owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    notes TEXT,
    tags JSONB DEFAULT '[]',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_deals_org_workspace ON crm_deals(organization_id, workspace_id);
CREATE INDEX idx_deals_pipeline_stage ON crm_deals(pipeline_id, stage_id);
CREATE INDEX idx_deals_owner ON crm_deals(owner_id);
```

#### crm_pipelines
```sql
CREATE TABLE crm_pipelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workspace_id, name)
);
CREATE INDEX idx_pipelines_workspace ON crm_pipelines(workspace_id);
```

#### crm_pipeline_stages
```sql
CREATE TABLE crm_pipeline_stages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_id UUID NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    order_index INT NOT NULL,
    color VARCHAR(7), -- Hex color
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pipeline_id, order_index)
);
CREATE INDEX idx_stages_pipeline ON crm_pipeline_stages(pipeline_id);
```

#### crm_companies
```sql
CREATE TABLE crm_companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    website VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    employee_count INT,
    annual_revenue DECIMAL(15,2),
    
    custom_fields JSONB DEFAULT '{}',
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_companies_org_workspace ON crm_companies(organization_id, workspace_id);
```

### Automation & Workflows

#### workflows
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft', -- draft, active, paused, archived
    
    -- Trigger
    trigger_type VARCHAR(50) NOT NULL, -- new_lead, call_completed, form_submitted, etc
    trigger_config JSONB NOT NULL,
    
    -- Workflow Definition
    nodes JSONB NOT NULL, -- Workflow steps
    edges JSONB NOT NULL, -- Connections between steps
    
    -- Settings
    run_count INT DEFAULT 0,
    success_count INT DEFAULT 0,
    error_count INT DEFAULT 0,
    last_run_at TIMESTAMP,
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    
    UNIQUE(workspace_id, name)
);
CREATE INDEX idx_workflows_org_workspace ON workflows(organization_id, workspace_id);
CREATE INDEX idx_workflows_status ON workflows(status);
```

#### workflow_executions (Logs)
```sql
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    status VARCHAR(50) DEFAULT 'pending', -- pending, running, success, failed
    trigger_data JSONB NOT NULL,
    execution_log JSONB DEFAULT '[]',
    error_message TEXT,
    
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INT
);
CREATE INDEX idx_executions_workflow ON workflow_executions(workflow_id);
CREATE INDEX idx_executions_status ON workflow_executions(status);
```

### Communication

#### communication_logs (Email, SMS, WhatsApp)
```sql
CREATE TABLE communication_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    channel VARCHAR(50) NOT NULL, -- email, sms, whatsapp
    message_type VARCHAR(50), -- transactional, marketing, notification
    
    sender VARCHAR(255) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    
    subject VARCHAR(500),
    content TEXT NOT NULL,
    
    status VARCHAR(50) DEFAULT 'pending', -- pending, sent, delivered, failed
    external_message_id VARCHAR(255),
    
    contact_id UUID REFERENCES crm_contacts(id) ON DELETE SET NULL,
    lead_id UUID REFERENCES crm_leads(id) ON DELETE SET NULL,
    
    template_id UUID REFERENCES communication_templates(id) ON DELETE SET NULL,
    campaign_id UUID REFERENCES communication_campaigns(id) ON DELETE SET NULL,
    
    metadata JSONB DEFAULT '{}',
    error_details TEXT,
    
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP,
    bounced_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_comm_logs_org_workspace ON communication_logs(organization_id, workspace_id);
CREATE INDEX idx_comm_logs_channel_status ON communication_logs(channel, status);
CREATE INDEX idx_comm_logs_recipient ON communication_logs(recipient);
```

#### communication_templates
```sql
CREATE TABLE communication_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    channel VARCHAR(50) NOT NULL, -- email, sms, whatsapp
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    subject VARCHAR(500),
    content TEXT NOT NULL,
    variables JSONB DEFAULT '[]', -- List of template variables
    
    is_default BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'active',
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(workspace_id, channel, name)
);
CREATE INDEX idx_templates_workspace_channel ON communication_templates(workspace_id, channel);
```

### Bookings & Appointments

#### booking_calendars
```sql
CREATE TABLE booking_calendars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Availability
    timezone VARCHAR(50) DEFAULT 'UTC',
    availability JSONB NOT NULL, -- Time slots and rules
    
    -- Settings
    min_booking_notice_minutes INT DEFAULT 0,
    max_booking_advance_days INT DEFAULT 90,
    buffer_time_minutes INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workspace_id, slug)
);
CREATE INDEX idx_calendars_workspace ON booking_calendars(workspace_id);
```

#### appointments
```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    calendar_id UUID NOT NULL REFERENCES booking_calendars(id) ON DELETE CASCADE,
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Time
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_minutes INT,
    timezone VARCHAR(50),
    
    -- Guest
    guest_name VARCHAR(255),
    guest_email VARCHAR(255),
    guest_phone VARCHAR(20),
    
    -- Status
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, confirmed, completed, cancelled
    
    -- Reminders
    send_reminder BOOLEAN DEFAULT TRUE,
    reminder_minutes_before INT DEFAULT 15,
    reminder_sent BOOLEAN DEFAULT FALSE,
    
    notes TEXT,
    custom_fields JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_appointments_calendar ON appointments(calendar_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_start_time ON appointments(start_time);
```

### Knowledge Base

#### knowledge_bases
```sql
CREATE TABLE knowledge_bases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    status VARCHAR(50) DEFAULT 'active',
    
    -- Vector Store Config
    qdrant_collection_name VARCHAR(255) UNIQUE,
    document_count INT DEFAULT 0,
    indexed_at TIMESTAMP,
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
CREATE INDEX idx_kb_workspace ON knowledge_bases(workspace_id);
```

#### knowledge_base_documents
```sql
CREATE TABLE knowledge_base_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50), -- pdf, docx, txt, csv
    file_size_bytes INT,
    file_url VARCHAR(500),
    
    content TEXT,
    content_hash VARCHAR(64), -- For deduplication
    
    status VARCHAR(50) DEFAULT 'processing', -- processing, indexed, failed
    error_message TEXT,
    
    chunk_count INT DEFAULT 0,
    indexed_at TIMESTAMP,
    
    uploaded_by UUID REFERENCES users(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kb_docs_kb_id ON knowledge_base_documents(knowledge_base_id);
CREATE INDEX idx_kb_docs_status ON knowledge_base_documents(status);
```

#### knowledge_base_chunks (Vector embeddings)
```sql
CREATE TABLE knowledge_base_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES knowledge_base_documents(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    content_length INT,
    
    vector_id VARCHAR(255), -- Qdrant point ID
    embedding VECTOR(1536), -- OpenAI embedding dimension
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);
CREATE INDEX idx_chunks_document ON knowledge_base_chunks(document_id);
CREATE INDEX idx_chunks_kb ON knowledge_base_chunks(knowledge_base_id);
```

### API & Webhooks

#### api_keys
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    name VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(20), -- For display
    key_hash VARCHAR(255) NOT NULL UNIQUE, -- Hashed key
    
    permissions JSONB DEFAULT '[]', -- Array of permission strings
    
    status VARCHAR(50) DEFAULT 'active', -- active, revoked
    
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    
    UNIQUE(workspace_id, name)
);
CREATE INDEX idx_api_keys_workspace ON api_keys(workspace_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
```

#### webhooks
```sql
CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    
    events JSONB NOT NULL, -- Events to subscribe to
    headers JSONB DEFAULT '{}', -- Custom headers
    
    is_active BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'active',
    
    secret VARCHAR(255), -- Webhook signing secret
    
    retry_policy JSONB DEFAULT '{"max_retries": 3, "backoff_multiplier": 2}',
    last_triggered_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_webhooks_workspace ON webhooks(workspace_id);
CREATE INDEX idx_webhooks_is_active ON webhooks(is_active);
```

#### webhook_logs
```sql
CREATE TABLE webhook_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    webhook_id UUID NOT NULL REFERENCES webhooks(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    event_type VARCHAR(100) NOT NULL,
    status_code INT,
    response_time_ms INT,
    
    request_body JSONB,
    response_body TEXT,
    error_message TEXT,
    
    retry_count INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending', -- pending, success, failed
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_webhook_logs_webhook_id ON webhook_logs(webhook_id);
CREATE INDEX idx_webhook_logs_status ON webhook_logs(status);
```

### Audit & Logging

#### audit_logs
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- create, update, delete, login, etc
    
    entity_type VARCHAR(100), -- users, agents, calls, etc
    entity_id UUID,
    
    changes JSONB, -- What changed (before/after)
    ip_address VARCHAR(45),
    user_agent TEXT,
    status VARCHAR(50) DEFAULT 'success', -- success, failed
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_audit_logs_org ON audit_logs(organization_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

#### activity_logs
```sql
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    activity_type VARCHAR(100) NOT NULL,
    description TEXT,
    
    entity_type VARCHAR(100),
    entity_id UUID,
    
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_activity_logs_org ON activity_logs(organization_id);
CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_activity_type ON activity_logs(activity_type);
```

### Email Verification & Password Reset

#### email_verification_tokens
```sql
CREATE TABLE email_verification_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_verification_tokens_user ON email_verification_tokens(user_id);
CREATE INDEX idx_verification_tokens_token ON email_verification_tokens(token);
```

#### password_reset_tokens
```sql
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_reset_tokens_user ON password_reset_tokens(user_id);
CREATE INDEX idx_reset_tokens_token ON password_reset_tokens(token);
```

## Indexes Summary

### Performance Indexes
- Foreign keys
- Status columns
- Timestamps (created_at, updated_at)
- Organization + workspace combinations
- Frequently filtered columns (email, phone, etc)

### Full-Text Search (Future)
```sql
CREATE INDEX idx_calls_transcript_fts ON calls USING GIN(to_tsvector('english', transcript));
CREATE INDEX idx_leads_notes_fts ON crm_leads USING GIN(to_tsvector('english', notes));
```

## Multi-Tenancy & Row-Level Security

### RLS Policies (Example)
```sql
-- Enable RLS on all tenant-aware tables
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their organization's data
CREATE POLICY agents_org_isolation ON agents
FOR ALL USING (
    organization_id IN (SELECT organization_id FROM organization_members WHERE user_id = current_user_id)
);
```

## Data Retention

- Call records: 2 years
- Audit logs: 1 year
- Communication logs: 6 months
- Activity logs: 3 months
- Deleted records: Soft delete with timestamp

## Backups

- Daily full backups
- Point-in-time recovery available
- Backup retention: 30 days

See [DATABASE_MANAGEMENT.md](./DATABASE_MANAGEMENT.md) for operational procedures.
