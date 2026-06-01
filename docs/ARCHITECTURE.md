# Call Agent - System Architecture

## Overview

Call Agent is a multi-tenant SaaS platform built with a microservices-inspired architecture deployed as containers. The system is designed for scalability, reliability, and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Web App     │  │  Mobile App  │  │  ChatWidget  │      │
│  │  (Next.js)   │  │  (React)     │  │  (Embedded)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ (HTTPS)
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway Layer                           │
│              (Nginx Reverse Proxy)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SSL/TLS Termination, Rate Limiting, Load Balancing│   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────┬──────────────────┬───────────────────────┘
                 │                  │
       ┌─────────▼──────┐  ┌────────▼────────┐
       │   REST API     │  │   WebSocket     │
       │   (FastAPI)    │  │   (FastAPI)     │
       └─────────┬──────┘  └────────┬────────┘
                 │                  │
┌────────────────▼──────────────────▼───────────────────────┐
│                   Application Layer                        │
│                      (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Route Handlers & Business Logic                      │ │
│  │  • Auth Module      • CRM Module                      │ │
│  │  • Agent Module     • Workflow Module                 │ │
│  │  • Voice Module     • Communication Module            │ │
│  │  • Call Module      • Booking Module                  │ │
│  │  • Analytics Module • Admin Module                    │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────┬──────────────────┬──────────────────────┘
                 │                  │
┌────────────────▼──────────────────▼──────────────────────┐
│                  Service/Domain Layer                     │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Service Classes - Core Business Logic                │ │
│  │  • AuthService        • CRMService                    │ │
│  │  • AgentService       • WorkflowService               │ │
│  │  • VoiceService       • SMSService                    │ │
│  │  • CallService        • WhatsAppService               │ │
│  │  • EmailService       • AnalyticsService              │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────┬──────────────────┬──────────────────────┘
                 │                  │
┌────────────────▼──────────────────▼──────────────────────┐
│                    Data Layer (ORM)                       │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ SQLAlchemy Models & Database Access                  │ │
│  │  • User, Organization, Workspace Models              │ │
│  │  • Agent, Call, Lead Models                          │ │
│  │  • Communication, Automation Models                  │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────┬──────────────────┬──────────────────────┘
                 │                  │
    ┌────────────▼────────┐    ┌────▼──────────────┐
    │   PostgreSQL        │    │     Redis Cache   │
    │   • Organizations   │    │  • Sessions       │
    │   • Users           │    │  • Rate Limits    │
    │   • Agents          │    │  • Job Queue      │
    │   • Calls           │    │  • Real-time Data │
    │   • Leads           │    │                   │
    │   • Contacts        │    │                   │
    └─────────────────────┘    └───────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                   External Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Ollama     │  │   Qdrant     │  │  Asterisk    │     │
│  │  (AI Models) │  │  (Vector DB) │  │   (PBX)      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Whisper STT  │  │  Piper TTS   │  │  WhatsApp    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Twilio     │  │     SMTP     │  │   Google     │     │
│  │   (SMS)      │  │   (Email)    │  │    OAuth     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Client Layer
- **Next.js Dashboard**: Web-based admin and user interface
- **Mobile App**: React-based mobile application
- **Chat Widget**: Embeddable AI chat widget for websites
- **Voice Clients**: WebRTC clients for voice communication

### 2. API Gateway (Nginx)
- SSL/TLS termination
- Rate limiting
- Load balancing
- Request/response compression
- CORS handling

### 3. Application Layer (FastAPI)
- REST API endpoints
- WebSocket connections for real-time features
- Request validation
- Error handling
- Middleware (auth, logging, CORS)

### 4. Service Layer
Business logic implementation:
- **AuthService**: Authentication, authorization, tokens
- **AgentService**: Agent CRUD, configuration
- **VoiceService**: Voice processing, AI integration
- **CallService**: Call management, routing
- **CRMService**: Lead, contact, deal management
- **WorkflowService**: Automation workflow execution
- **CommunicationService**: Email, SMS, WhatsApp
- **AnalyticsService**: Data aggregation and reporting

### 5. Data Layer
- **PostgreSQL**: Primary relational database
  - User & organization data
  - Agent configurations
  - Call records
  - CRM data
  - Automation workflows

- **Redis**: Caching & real-time features
  - Session management
  - Rate limiting
  - Job queue
  - Real-time notifications
  - Cache layer

- **Qdrant**: Vector database
  - Knowledge base embeddings
  - Semantic search
  - RAG pipeline support

### 6. External Services
- **Ollama**: Local LLM inference (Llama 2, Qwen, Mistral)
- **Whisper**: Speech-to-text
- **Piper**: Text-to-speech
- **Asterisk**: PBX and SIP integration
- **WhatsApp Business API**: WhatsApp messaging
- **Twilio**: SMS gateway
- **SMTP**: Email sending
- **Google OAuth**: Social login

## Multi-Tenancy Model

### Isolation Strategy: Row-Level Security (RLS)

```
User
  ├── Organization (Tenant)
  │    ├── Workspace 1
  │    │    ├── Agents
  │    │    ├── Calls
  │    │    ├── Leads
  │    │    └── Workflows
  │    └── Workspace 2
  │         ├── Agents
  │         ├── Calls
  │         └── ...
  └── TeamMembers
       ├── Owner
       ├── Admin
       └── User
```

### Data Isolation
- Every record includes `organization_id`
- Database policies enforce isolation
- Middleware validates tenant access
- API endpoints filter by organization context

## Authentication & Authorization

### Authentication Flow
```
1. User enters credentials
2. Backend validates against database
3. Server generates JWT (access + refresh tokens)
4. Frontend stores tokens in secure httpOnly cookies
5. Subsequent requests include JWT in Authorization header
6. Middleware validates token before processing request
```

### Authorization Model
```
Organization Roles:
  • Owner: Full control, billing, team management
  • Admin: All operations except billing
  • User: Limited based on assigned permissions
  • Guest: View-only access

Permissions:
  • Agent Management (create, edit, delete, clone)
  • Call Management (view, record, transfer)
  • Lead Management (create, update, delete)
  • Workflow Management (create, execute, monitor)
  • User Management (invite, remove, change role)
  • Settings (organization, workspace)
```

## Call Flow Architecture

### Incoming Call Flow
```
1. Call arrives at Asterisk PBX
2. Asterisk routes to FastAPI via REST/AGI
3. FastAPI queries agent configuration
4. Load agent context from PostgreSQL
5. Initialize conversation state in Redis
6. Start WebSocket connection with client
7. Stream audio chunks to Whisper for STT
8. Process transcribed text with LLM (Ollama)
9. Generate response via Piper TTS
10. Stream audio back to caller
11. Record call data in PostgreSQL
12. Update CRM if applicable
13. Trigger post-call automation workflows
```

### Outgoing Call Flow
```
1. User initiates call from dashboard
2. FastAPI validates phone number and permissions
3. Create call record in PostgreSQL
4. Initiate call via Asterisk/SIP
5. Establish audio stream
6. Same voice processing as incoming
7. Record call metadata
8. Update lead/contact status
9. Trigger post-call automations
```

## AI Agent Processing Pipeline

```
┌──────────────┐
│ User Input   │
│ (Voice/Text) │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│ 1. Audio Processing      │
│    (Whisper STT)         │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 2. Retrieval            │
│    (Qdrant Vector Search)│
│    Knowledge Base Docs    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 3. Context Building      │
│    • Conversation history │
│    • Retrieved documents  │
│    • User profile        │
│    • Agent personality   │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 4. LLM Processing        │
│    (Ollama)              │
│    Generate response      │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ 5. Response Synthesis    │
│    (Piper TTS)           │
│    Generate speech        │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Output (Voice/Text)      │
└──────────────────────────┘
```

## Scaling Strategy

### Horizontal Scaling
- **API Instances**: Multiple FastAPI instances behind load balancer
- **Worker Pool**: Celery/RQ for async tasks
- **Database Replication**: PostgreSQL read replicas
- **Redis Cluster**: Redis Sentinel for high availability

### Vertical Scaling
- Increase container resources (CPU, RAM)
- Optimize database queries with indexes
- Implement caching strategies

### Database Partitioning
- Partition call records by date
- Partition CRM data by organization
- Implement data archival for old records

## Security Architecture

### Network Security
- TLS/SSL encryption in transit
- VPC isolation (in cloud deployments)
- Firewall rules and WAF
- DDoS protection

### Application Security
- Input validation and sanitization
- SQL injection prevention (SQLAlchemy parameterized)
- CSRF token protection
- XSS protection (Content Security Policy)
- Rate limiting per user/IP
- CORS configuration

### Data Security
- Password hashing (bcrypt)
- Field-level encryption for sensitive data
- Audit logging of all operations
- Data retention policies
- GDPR compliance (data deletion)

### Authentication Security
- JWT with expiration
- Refresh token rotation
- Secure token storage
- Multi-factor authentication (MFA)
- Session invalidation on logout

## High Availability & Disaster Recovery

### Redundancy
- Database replication
- Redis cluster
- Multiple API instances
- Health checks and auto-restart

### Backup Strategy
- Daily PostgreSQL backups
- Backup replication to external storage
- Point-in-time recovery capability

### Monitoring & Alerting
- Application performance monitoring
- Error tracking
- Log aggregation
- Alert notifications
- Health dashboards

## Performance Optimization

### Caching Strategy
- HTTP caching headers
- Redis caching layer
- Database query caching
- CDN for static assets

### Database Optimization
- Proper indexing
- Query optimization
- Connection pooling
- Query result caching

### API Optimization
- Response compression
- Pagination for large datasets
- Selective field loading
- Async processing for heavy tasks

## Monitoring & Logging

### Application Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Performance metrics

### System Monitoring
- Container resource usage
- Database performance
- API response times
- Error rates
- Queue depths

## Deployment Architecture

Supported deployment targets:
- **Docker Compose**: Local development and small deployments
- **Kubernetes**: Production-grade containerized deployment
- **Cloud Platforms**: AWS, Google Cloud, Azure with managed services

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.
