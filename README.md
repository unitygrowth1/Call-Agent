# Call Agent - Enterprise AI Voice Agent & Business Automation SaaS Platform

A production-grade, multi-tenant SaaS platform for building intelligent voice agents, managing customer communications, and automating business workflows.

## Features

### AI Voice Agent System
- Real-time voice conversations with AI agents
- Multiple AI model support (Llama 3, Qwen, Mistral via Ollama)
- Faster Whisper for speech-to-text
- Piper TTS for natural speech synthesis
- Context-aware conversations with knowledge base

### Multi-Tenant Architecture
- Organization & workspace management
- User roles and permissions (Owner, Admin, User)
- Team collaboration features
- Audit and activity logs

### Telephony & Call Center
- Asterisk PBX integration
- SIP & WebRTC support
- Incoming/outgoing calls
- Call recording and routing
- Predictive and power dialer
- Campaign calling

### CRM System
- Lead management and pipelines
- Customer database
- Contact management
- Deal tracking
- Task and note management

### Communication Channels
- WhatsApp Business integration
- SMS messaging
- Email campaigns
- Website chat widget

### Automation & Workflow
- Drag-and-drop workflow builder
- Triggers, conditions, and actions
- Webhook support
- Automation logs

### Booking System
- Appointment scheduling
- Calendar management
- Availability rules
- Automatic reminders

### Analytics & Reporting
- Real-time dashboards
- Call metrics and analytics
- Conversion tracking
- Agent performance metrics

## Tech Stack

### Frontend
- Next.js with TypeScript
- Tailwind CSS
- Responsive design
- Dark mode support

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis
- Qdrant (Vector Database)

### AI & Speech
- Ollama with Llama 3, Qwen, Mistral
- Faster Whisper (STT)
- Piper TTS

### Infrastructure
- Docker & Docker Compose
- Nginx
- PostgreSQL
- Redis
- Qdrant

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/unitygrowth1/Call-Agent.git
cd Call-Agent
```

2. Setup environment variables:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Build and start services:
```bash
docker-compose up --build
```

4. Initialize database:
```bash
docker-compose exec backend python -m alembic upgrade head
```

5. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
Call-Agent/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── ai-modules/          # AI and speech processing
├── telephony/           # Asterisk & SIP integration
├── docker-compose.yml
├── nginx/               # Nginx configuration
└── docs/                # Documentation
```

## Documentation

- [Architecture Guide](./docs/ARCHITECTURE.md)
- [Database Schema](./docs/DATABASE.md)
- [API Documentation](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Installation Guide](./docs/INSTALLATION.md)
- [Security Guide](./docs/SECURITY.md)

## License

MIT

## Support

For issues and support, please refer to the documentation or create an issue on GitHub.
