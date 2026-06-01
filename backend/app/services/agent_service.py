# Agent Service

from sqlalchemy.orm import Session
from app.models.agent import Agent, AgentVersion
from app.models.organization import Organization, Workspace
from app.schemas.agent import AgentCreateRequest, AgentUpdateRequest
from app.core.exceptions import NotFoundException, ConflictException, ValidationException
from app.core.constants import AgentStatus
from typing import List, Optional
import uuid
import json
import logging

logger = logging.getLogger(__name__)

class AgentService:
    """
    Agent management service
    """
    
    @staticmethod
    def create_agent(
        db: Session,
        organization_id: uuid.UUID,
        workspace_id: uuid.UUID,
        request: AgentCreateRequest,
        created_by: uuid.UUID,
    ) -> Agent:
        """
        Create a new agent
        """
        # Verify workspace
        workspace = db.query(Workspace).filter(
            Workspace.id == workspace_id,
            Workspace.organization_id == organization_id,
        ).first()
        
        if not workspace:
            raise NotFoundException("Workspace not found")
        
        # Create slug
        slug = request.name.lower().replace(" ", "-")
        
        # Check if slug already exists
        existing = db.query(Agent).filter(
            Agent.workspace_id == workspace_id,
            Agent.slug == slug,
        ).first()
        
        if existing:
            raise ConflictException(f"Agent with name {request.name} already exists")
        
        # Create agent
        agent = Agent(
            id=uuid.uuid4(),
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=request.name,
            slug=slug,
            description=request.description,
            agent_type=request.agent_type,
            personality=request.personality,
            system_prompt=request.system_prompt,
            model_name=request.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            voice_id=request.voice_id,
            language=request.language,
            use_knowledge_base=request.use_knowledge_base,
            knowledge_base_id=request.knowledge_base_id,
            enable_call_recording=request.enable_call_recording,
            enable_transcription=request.enable_transcription,
            max_call_duration=request.max_call_duration,
            enable_context_retention=request.enable_context_retention,
            context_window=request.context_window,
            created_by=created_by,
            status=AgentStatus.ACTIVE,
        )
        db.add(agent)
        db.flush()
        
        # Create version 1
        version = AgentVersion(
            id=uuid.uuid4(),
            agent_id=agent.id,
            version_number=1,
            configuration=request.dict(),
            is_published=True,
            created_by=created_by,
        )
        db.add(version)
        db.commit()
        
        logger.info(f"Agent created: {agent.name} (ID: {agent.id})")
        return agent
    
    @staticmethod
    def get_agent(
        db: Session,
        agent_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> Agent:
        """
        Get agent by ID
        """
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.organization_id == organization_id,
        ).first()
        
        if not agent:
            raise NotFoundException("Agent not found")
        
        return agent
    
    @staticmethod
    def list_agents(
        db: Session,
        organization_id: uuid.UUID,
        workspace_id: uuid.UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple:
        """
        List agents for organization/workspace
        """
        query = db.query(Agent).filter(
            Agent.organization_id == organization_id,
            Agent.workspace_id == workspace_id,
        )
        
        total = query.count()
        agents = query.offset(skip).limit(limit).all()
        
        return agents, total
    
    @staticmethod
    def update_agent(
        db: Session,
        agent_id: uuid.UUID,
        organization_id: uuid.UUID,
        request: AgentUpdateRequest,
    ) -> Agent:
        """
        Update agent configuration
        """
        agent = AgentService.get_agent(db, agent_id, organization_id)
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        db.commit()
        logger.info(f"Agent updated: {agent.name}")
        return agent
    
    @staticmethod
    def delete_agent(
        db: Session,
        agent_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> bool:
        """
        Delete an agent
        """
        agent = AgentService.get_agent(db, agent_id, organization_id)
        db.delete(agent)
        db.commit()
        
        logger.info(f"Agent deleted: {agent.name}")
        return True
    
    @staticmethod
    def clone_agent(
        db: Session,
        agent_id: uuid.UUID,
        organization_id: uuid.UUID,
        new_name: str,
        created_by: uuid.UUID,
    ) -> Agent:
        """
        Clone an existing agent
        """
        source_agent = AgentService.get_agent(db, agent_id, organization_id)
        
        # Create new agent with copied configuration
        new_slug = new_name.lower().replace(" ", "-")
        
        new_agent = Agent(
            id=uuid.uuid4(),
            organization_id=organization_id,
            workspace_id=source_agent.workspace_id,
            name=new_name,
            slug=new_slug,
            description=source_agent.description,
            agent_type=source_agent.agent_type,
            personality=source_agent.personality,
            system_prompt=source_agent.system_prompt,
            model_name=source_agent.model_name,
            temperature=source_agent.temperature,
            max_tokens=source_agent.max_tokens,
            voice_id=source_agent.voice_id,
            language=source_agent.language,
            use_knowledge_base=source_agent.use_knowledge_base,
            knowledge_base_id=source_agent.knowledge_base_id,
            enable_call_recording=source_agent.enable_call_recording,
            enable_transcription=source_agent.enable_transcription,
            max_call_duration=source_agent.max_call_duration,
            enable_context_retention=source_agent.enable_context_retention,
            context_window=source_agent.context_window,
            created_by=created_by,
            status=AgentStatus.ACTIVE,
        )
        db.add(new_agent)
        db.flush()
        
        # Create version
        version = AgentVersion(
            id=uuid.uuid4(),
            agent_id=new_agent.id,
            version_number=1,
            configuration={
                "name": new_name,
                "description": source_agent.description,
                "personality": source_agent.personality,
                "system_prompt": source_agent.system_prompt,
            },
            is_published=True,
            created_by=created_by,
        )
        db.add(version)
        db.commit()
        
        logger.info(f"Agent cloned: {new_name} from {source_agent.name}")
        return new_agent
