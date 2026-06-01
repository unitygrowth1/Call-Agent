# Call Agent - Project Folder Structure

## Complete Directory Tree

```
Call-Agent/
├── README.md                                 # Project overview
├── docker-compose.yml                        # Docker Compose configuration
├── .env.example                              # Environment variables template
├── .gitignore                                # Git ignore rules
│
├── backend/                                  # FastAPI Backend
│   ├── Dockerfile                            # Backend Docker image
│   ├── requirements.txt                      # Python dependencies
│   ├── main.py                               # Application entry point
│   ├── config.py                             # Configuration management
│   ├── .env.example                          # Backend specific env vars
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/                              # API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py                   # Authentication endpoints
│   │   │   │   ├── users.py                  # User management
│   │   │   │   ├── organizations.py          # Org/workspace management
│   │   │   │   ├── agents.py                 # Agent CRUD
│   │   │   │   ├── calls.py                  # Call management
│   │   │   │   ├── crm.py                    # CRM (leads, contacts, deals)
│   │   │   │   ├── workflows.py              # Automation workflows
│   │   │   │   ├── communications.py         # Email, SMS, WhatsApp
│   │   │   │   ├── voice.py                  # Voice processing
│   │   │   │   ├── bookings.py               # Appointment booking
│   │   │   │   ├── knowledge_base.py         # Knowledge base upload/search
│   │   │   │   ├── analytics.py              # Analytics & reporting
│   │   │   │   ├── api_keys.py               # API key management
│   │   │   │   ├── webhooks.py               # Webhook management
│   │   │   │   ├── admin.py                  # Admin operations
│   │   │   │   └── health.py                 # Health check endpoint
│   │   │   └── routes.py                     # Route registration
│   │   │
│   │   ├── models/                           # SQLAlchemy ORM Models
│   │   │   ├── __init__.py
│   │   │   ├── base.py                       # Base model class
│   │   │   ├── user.py                       # User model
│   │   │   ├── organization.py               # Organization/Workspace
│   │   │   ├── agent.py                      # Agent model
│   │   │   ├── call.py                       # Call record model
│   │   │   ├── crm.py                        # Lead, Contact, Deal models
│   │   │   ├── workflow.py                   # Workflow & automation models
│   │   │   ├── communication.py              # Email, SMS, WhatsApp logs
│   │   │   ├── booking.py                    # Appointment models
│   │   │   ├── knowledge_base.py             # KB document models
│   │   │   ├── audit_log.py                  # Audit trail models
│   │   │   └── api_key.py                    # API key model
│   │   │
│   │   ├── schemas/                          # Pydantic schemas (validation)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── agent.py
│   │   │   ├── call.py
│   │   │   ├── crm.py
│   │   │   ├── workflow.py
│   │   │   ├── communication.py
│   │   │   ├── booking.py
│   │   │   └── common.py                     # Common schemas
│   │   │
│   │   ├── services/                         # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py               # Authentication logic
│   │   │   ├── user_service.py               # User management
│   │   │   ├── org_service.py                # Organization management
│   │   │   ├── agent_service.py              # Agent management
│   │   │   ├── call_service.py               # Call processing
│   │   │   ├── crm_service.py                # CRM operations
│   │   │   ├── workflow_service.py           # Workflow execution
│   │   │   ├── communication_service.py      # Email, SMS, WhatsApp
│   │   │   ├── voice_service.py              # Voice processing
│   │   │   ├── knowledge_base_service.py     # KB management
│   │   │   ├── booking_service.py            # Booking management
│   │   │   ├── analytics_service.py          # Analytics
│   │   │   └── ai_service.py                 # AI/LLM operations
│   │   │
│   │   ├── workers/                          # Async task workers
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py                 # Celery configuration
│   │   │   ├── tasks.py                      # Background tasks
│   │   │   ├── call_tasks.py                 # Call processing tasks
│   │   │   ├── email_tasks.py                # Email sending
│   │   │   ├── sms_tasks.py                  # SMS sending
│   │   │   └── automation_tasks.py           # Workflow execution
│   │   │
│   │   ├── core/                             # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── config.py                     # Configuration
│   │   │   ├── security.py                   # Password hashing, JWT
│   │   │   ├── constants.py                  # App constants
│   │   │   └── exceptions.py                 # Custom exceptions
│   │   │
│   │   ├── middleware/                       # Request middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                       # JWT validation
│   │   │   ├── tenant.py                     # Tenant/org isolation
│   │   │   ├── logging.py                    # Request logging
│   │   │   ├── error_handler.py              # Error handling
│   │   │   └── rate_limit.py                 # Rate limiting
│   │   │
│   │   ├── dependencies/                     # Dependency injection
│   │   │   ├── __init__.py
│   │   │   ├── db.py                         # Database session
│   │   │   ├── auth.py                       # Auth dependencies
│   │   │   └── org.py                        # Org context
│   │   │
│   │   ├── utils/                            # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── validators.py                 # Input validators
│   │   │   ├── helpers.py                    # Helper functions
│   │   │   ├── pagination.py                 # Pagination utilities
│   │   │   ├── cache.py                      # Redis cache utilities
│   │   │   ├── phone.py                      # Phone number utilities
│   │   │   └── email.py                      # Email utilities
│   │   │
│   │   ├── integrations/                     # External API integrations
│   │   │   ├── __init__.py
│   │   │   ├── ollama.py                     # Ollama LLM integration
│   │   │   ├── qdrant.py                     # Qdrant vector DB
│   │   │   ├── asterisk.py                   # Asterisk PBX
│   │   │   ├── whisper.py                    # Whisper STT
│   │   │   ├── piper.py                      # Piper TTS
│   │   │   ├── twilio.py                     # Twilio SMS
│   │   │   ├── whatsapp.py                   # WhatsApp API
│   │   │   ├── gmail.py                      # Gmail/SMTP
│   │   │   └── stripe.py                     # Stripe payments (optional)
│   │   │
│   │   ├── websockets/                       # WebSocket handlers
│   │   │   ├── __init__.py
│   │   │   ├── voice.py                      # Voice streaming
│   │   │   ├── notifications.py              # Real-time notifications
│   │   │   └── manager.py                    # Connection manager
│   │   │
│   │   ├── events/                           # Event handling
│   │   │   ├── __init__.py
│   │   │   ├── call_events.py                # Call events
│   │   │   ├── lead_events.py                # Lead events
│   │   │   └── workflow_events.py            # Workflow events
│   │   │
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                             # Database connection
│   │   ├── base.py                           # Base classes
│   │   ├── init.sql                          # Database initialization
│   │   ├── migrations/                       # Alembic migrations
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   ├── alembic.ini
│   │   │   └── versions/
│   │   │       ├── 001_initial_schema.py
│   │   │       ├── 002_add_call_records.py
│   │   │       └── ...
│   │   │
│   │   └── seeds/                            # Database seeders
│   │       ├── seed_data.py
│   │       └── initial_data.json
│   │
│   ├── tests/                                # Unit & integration tests
│   │   ├── __init__.py
│   │   ├── conftest.py                       # Pytest configuration
│   │   ├── test_auth.py
│   │   ├── test_agents.py
│   │   ├── test_calls.py
│   │   ├── test_crm.py
│   │   ├── test_workflows.py
│   │   ├── test_integrations.py
│   │   └── fixtures/                         # Test fixtures
│   │       ├── auth.py
│   │       ├── agents.py
│   │       └── ...
│   │
│   └── logs/                                 # Application logs (gitignored)
│
├── frontend/                                 # Next.js Frontend
│   ├── Dockerfile                            # Frontend Docker image
│   ├── package.json                          # Dependencies
│   ├── package-lock.json
│   ├── tsconfig.json                         # TypeScript config
│   ├── tailwind.config.js                    # Tailwind CSS config
│   ├── next.config.js                        # Next.js config
│   ├── .env.example
│   ├── .eslintrc.json                        # ESLint config
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   ├── images/
│   │   │   ├── logo.png
│   │   │   ├── hero.png
│   │   │   └── ...
│   │   └── fonts/
│   │
│   ├── src/
│   │   ├── app/                              # Next.js App Router
│   │   │   ├── layout.tsx                    # Root layout
│   │   │   ├── page.tsx                      # Home page
│   │   │   ├── globals.css                   # Global styles
│   │   │   │
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── register/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── forgot-password/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── reset-password/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx                  # Dashboard home
│   │   │   │   │
│   │   │   │   ├── agents/
│   │   │   │   │   ├── page.tsx              # Agents list
│   │   │   │   │   ├── [id]/
│   │   │   │   │   │   ├── page.tsx          # Agent details
│   │   │   │   │   │   └── edit/
│   │   │   │   │   │       └── page.tsx
│   │   │   │   │   └── new/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── calls/
│   │   │   │   │   ├── page.tsx              # Calls list
│   │   │   │   │   ├── [id]/
│   │   │   │   │   │   └── page.tsx          # Call details
│   │   │   │   │   └── incoming/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── crm/
│   │   │   │   │   ├── leads/
│   │   │   │   │   │   ├── page.tsx
│   │   │   │   │   │   └── [id]/
│   │   │   │   │   │       └── page.tsx
│   │   │   │   │   ├── contacts/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── deals/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── pipelines/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── workflows/
│   │   │   │   │   ├── page.tsx              # Workflows list
│   │   │   │   │   ├── [id]/
│   │   │   │   │   │   └── page.tsx          # Workflow builder
│   │   │   │   │   └── new/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── communications/
│   │   │   │   │   ├── sms/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── whatsapp/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── email/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── bookings/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── calendar/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── knowledge-base/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── upload/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── analytics/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── calls/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── agents/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   ├── settings/
│   │   │   │   │   ├── page.tsx              # Organization settings
│   │   │   │   │   ├── workspace/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── team/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── api-keys/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── billing/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── integrations/
│   │   │   │   │       └── page.tsx
│   │   │   │   │
│   │   │   │   └── admin/
│   │   │   │       ├── page.tsx
│   │   │   │       ├── users/
│   │   │   │       │   └── page.tsx
│   │   │   │       ├── organizations/
│   │   │   │       │   └── page.tsx
│   │   │   │       ├── usage/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── logs/
│   │   │   │           └── page.tsx
│   │   │   │
│   │   │   └── api/                          # API routes
│   │   │       └── ...
│   │   │
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   ├── Form.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Select.tsx
│   │   │   │   ├── Textarea.tsx
│   │   │   │   ├── Checkbox.tsx
│   │   │   │   ├── Radio.tsx
│   │   │   │   ├── Toggle.tsx
│   │   │   │   ├── Pagination.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   ├── Error.tsx
│   │   │   │   ├── Toast.tsx
│   │   │   │   └── Badge.tsx
│   │   │   │
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   ├── ForgotPasswordForm.tsx
│   │   │   │   └── ResetPasswordForm.tsx
│   │   │   │
│   │   │   ├── agent/
│   │   │   │   ├── AgentList.tsx
│   │   │   │   ├── AgentCard.tsx
│   │   │   │   ├── AgentForm.tsx
│   │   │   │   ├── AgentSettings.tsx
│   │   │   │   ├── AgentBuilder.tsx
│   │   │   │   └── AgentPreview.tsx
│   │   │   │
│   │   │   ├── call/
│   │   │   │   ├── CallList.tsx
│   │   │   │   ├── CallCard.tsx
│   │   │   │   ├── CallInterface.tsx
│   │   │   │   ├── VoicePlayer.tsx
│   │   │   │   └── CallRecorder.tsx
│   │   │   │
│   │   │   ├── crm/
│   │   │   │   ├── LeadList.tsx
│   │   │   │   ├── LeadForm.tsx
│   │   │   │   ├── ContactCard.tsx
│   │   │   │   ├── DealPipeline.tsx
│   │   │   │   └── TaskList.tsx
│   │   │   │
│   │   │   ├── workflow/
│   │   │   │   ├── WorkflowBuilder.tsx
│   │   │   │   ├── WorkflowNode.tsx
│   │   │   │   ├── WorkflowEditor.tsx
│   │   │   │   └── TriggerSelector.tsx
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   ├── Chart.tsx
│   │   │   │   ├── MetricCard.tsx
│   │   │   │   └── RecentCalls.tsx
│   │   │   │
│   │   │   ├── communication/
│   │   │   │   ├── SMSForm.tsx
│   │   │   │   ├── WhatsAppForm.tsx
│   │   │   │   ├── EmailForm.tsx
│   │   │   │   └── MessageLog.tsx
│   │   │   │
│   │   │   ├── booking/
│   │   │   │   ├── CalendarView.tsx
│   │   │   │   ├── BookingForm.tsx
│   │   │   │   └── AvailabilitySettings.tsx
│   │   │   │
│   │   │   ├── chat/
│   │   │   │   ├── ChatWidget.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── ChatInput.tsx
│   │   │   │
│   │   │   └── admin/
│   │   │       ├── UserManagement.tsx
│   │   │       ├── OrgManagement.tsx
│   │   │       └── SystemStats.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useOrganization.ts
│   │   │   ├── useApi.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useForm.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── usePagination.ts
│   │   │   └── useDebounce.ts
│   │   │
│   │   ├── contexts/
│   │   │   ├── AuthContext.tsx
│   │   │   ├── OrganizationContext.tsx
│   │   │   ├── ThemeContext.tsx
│   │   │   └── NotificationContext.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                        # API client
│   │   │   ├── axios.ts                      # Axios config
│   │   │   ├── utils.ts                      # Utility functions
│   │   │   ├── constants.ts                  # Constants
│   │   │   ├── validators.ts                 # Form validators
│   │   │   └── formatters.ts                 # Data formatters
│   │   │
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├── variables.css
│   │   │   └── animations.css
│   │   │
│   │   └── types/
│   │       ├── index.ts
│   │       ├── api.ts
│   │       ├── agent.ts
│   │       ├── call.ts
│   │       ├── crm.ts
│   │       └── workflow.ts
│   │
│   └── tests/
│       ├── __tests__/
│       │   ├── auth.test.tsx
│       │   ├── agents.test.tsx
│       │   └── ...
│       └── jest.config.js
│
├── ai-modules/                               # AI & Speech Processing
│   ├── __init__.py
│   ├── requirements.txt
│   │
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── stt/
│   │   │   ├── __init__.py
│   │   │   ├── whisper_stt.py                # Faster Whisper implementation
│   │   │   └── stream_processor.py           # Real-time stream processing
│   │   │
│   │   ├── tts/
│   │   │   ├── __init__.py
│   │   │   ├── piper_tts.py                  # Piper TTS implementation
│   │   │   └── voice_manager.py              # Voice selection & management
│   │   │
│   │   ├── audio/
│   │   │   ├── __init__.py
│   │   │   ├── processor.py                  # Audio processing
│   │   │   ├── formats.py                    # Audio format handling
│   │   │   └── silence_detector.py           # Silence detection
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── audio_utils.py
│   │       └── voice_utils.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── ollama_client.py                  # Ollama integration
│   │   ├── prompt_builder.py                 # Prompt construction
│   │   ├── context_manager.py                # Context management
│   │   ├── models.py                         # Model configurations
│   │   └── response_processor.py             # Response processing
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py                     # Embedding generation
│   │   ├── document_processor.py             # Document parsing
│   │   ├── vector_store.py                   # Qdrant integration
│   │   ├── retriever.py                      # RAG retrieval
│   │   └── pipeline.py                       # RAG pipeline
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py                          # Core agent logic
│   │   ├── conversation_manager.py           # Conversation tracking
│   │   ├── state_manager.py                  # State management
│   │   └── interruption_handler.py           # Interrupt handling
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_stt.py
│       ├── test_tts.py
│       ├── test_llm.py
│       └── test_agent.py
│
├── telephony/                                # Telephony & PBX Integration
│   ├── __init__.py
│   ├── requirements.txt
│   │
│   ├── asterisk/
│   │   ├── __init__.py
│   │   ├── manager.py                        # Asterisk AMI client
│   │   ├── agi_handler.py                    # AGI request handler
│   │   ├── dialplan.py                       # Dialplan management
│   │   ├── extensions.py                     # Extension configuration
│   │   └── call_handler.py                   # Call handling logic
│   │
│   ├── sip/
│   │   ├── __init__.py
│   │   ├── client.py                         # SIP client
│   │   ├── server.py                         # SIP server
│   │   └── protocol.py                       # SIP protocol handler
│   │
│   ├── webrtc/
│   │   ├── __init__.py
│   │   ├── peer_connection.py                # WebRTC peer connection
│   │   ├── signaling.py                      # Signaling protocol
│   │   ├── ice_server.py                     # ICE server integration
│   │   └── media_stream.py                   # Media stream handling
│   │
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── call_router.py                    # Call routing logic
│   │   ├── queue_manager.py                  # Queue management
│   │   └── ivr_system.py                     # IVR system
│   │
│   ├── recording/
│   │   ├── __init__.py
│   │   ├── recorder.py                       # Call recording
│   │   ├── storage.py                        # Recording storage
│   │   └── playback.py                       # Recording playback
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_asterisk.py
│       ├── test_sip.py
│       └── test_webrtc.py
│
├── nginx/                                    # Nginx Configuration
│   ├── nginx.conf                            # Main configuration
│   ├── conf.d/
│   │   ├── default.conf
│   │   ├── api.conf
│   │   ├── frontend.conf
│   │   └── websocket.conf
│   └── ssl/
│       └── .gitkeep                          # SSL certificates (empty on repo)
│
├── docker/                                   # Docker files
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── Dockerfile.ai
│   └── Dockerfile.telephony
│
├── scripts/
│   ├── setup.sh                              # Initial setup script
│   ├── migrate_db.sh                         # Database migration
│   ├── seed_db.sh                            # Database seeding
│   ├── backup.sh                             # Database backup
│   ├── restore.sh                            # Database restore
│   ├── health_check.sh                       # Health check script
│   └── deploy.sh                             # Deployment script
│
└── docs/                                     # Documentation
    ├── ARCHITECTURE.md                       # Architecture documentation
    ├── FOLDER_STRUCTURE.md                   # This file
    ├── DATABASE.md                           # Database schema
    ├── API.md                                # API documentation
    ├── INSTALLATION.md                       # Installation guide
    ├── DEPLOYMENT.md                         # Deployment guide
    ├── SECURITY.md                           # Security guide
    ├── SCALING.md                            # Scaling guide
    ├── CONTRIBUTION.md                       # Contribution guidelines
    └── TROUBLESHOOTING.md                    # Troubleshooting guide
```

## Key Directories Explained

### `/backend`
FastAPI application with all business logic, database models, API endpoints, integrations, and services.

### `/frontend`
Next.js React application for the web dashboard with components, pages, hooks, and state management.

### `/ai-modules`
AI and speech processing modules: STT, TTS, LLM integration, RAG pipeline, and agent logic.

### `/telephony`
Telephony integration: Asterisk, SIP, WebRTC, call routing, IVR, and recording.

### `/nginx`
Nginx configuration for reverse proxy, load balancing, SSL/TLS, and request routing.

### `/docs`
Comprehensive documentation for architecture, setup, deployment, and operations.

## Naming Conventions

### Python Files
- **Services**: `*_service.py` (e.g., `agent_service.py`)
- **Models**: `*.py` in models folder (e.g., `user.py`)
- **Schemas**: `*.py` in schemas folder
- **Utilities**: `*_utils.py` (e.g., `email_utils.py`)
- **Integrations**: `*_integration.py` or service name (e.g., `asterisk.py`)

### React/TypeScript Files
- **Components**: `PascalCase.tsx` (e.g., `AgentForm.tsx`)
- **Hooks**: `use*.ts` (e.g., `useAuth.ts`)
- **Contexts**: `*Context.tsx` (e.g., `AuthContext.tsx`)
- **Types**: `*.ts` (e.g., `agent.ts`)
- **Utilities**: `*Utils.ts` or descriptive name

### Folders
- **All lowercase with hyphens**: `/api-keys`, `/knowledge-base`
- **Plural for collections**: `/components`, `/hooks`, `/pages`

## Configuration Files

Root level:
- `.env.example`: Environment variables template
- `docker-compose.yml`: Docker services configuration
- `.gitignore`: Git ignore patterns
- `README.md`: Project overview

Backend:
- `backend/.env.example`: Backend-specific environment variables
- `backend/requirements.txt`: Python dependencies
- `backend/Dockerfile`: Backend Docker image

Frontend:
- `frontend/.env.example`: Frontend-specific environment variables
- `frontend/package.json`: Node dependencies
- `frontend/Dockerfile`: Frontend Docker image
- `frontend/tsconfig.json`: TypeScript configuration
- `frontend/tailwind.config.js`: Tailwind CSS configuration

## Development Workflow

1. **Local Development**: Use `docker-compose up` to run all services
2. **File Structure**: Follow the naming conventions and organization
3. **New Features**: Create new files in appropriate directories
4. **Database Changes**: Use Alembic migrations
5. **Testing**: Write tests in the `/tests` directory
6. **Documentation**: Update docs when adding features

For detailed setup instructions, see [INSTALLATION.md](./INSTALLATION.md).
