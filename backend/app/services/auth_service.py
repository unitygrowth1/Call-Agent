# Authentication Service

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.organization import Organization, OrganizationMember, Workspace
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import UnauthorizedException, ConflictException, NotFoundException
from app.core.constants import UserRole
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """
    Authentication service for user registration, login, and token management
    """
    
    @staticmethod
    def register_user(db: Session, request: UserRegisterRequest) -> dict:
        """
        Register a new user with organization
        """
        # Check if user exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise ConflictException(f"User with email {request.email} already exists")
        
        # Create user
        user = User(
            id=uuid.uuid4(),
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            is_active=True,
        )
        db.add(user)
        db.flush()
        
        # Create organization
        org_slug = request.organization_name.lower().replace(" ", "-")
        organization = Organization(
            id=uuid.uuid4(),
            name=request.organization_name,
            slug=org_slug,
            status="active",
        )
        db.add(organization)
        db.flush()
        
        # Create default workspace
        workspace = Workspace(
            id=uuid.uuid4(),
            organization_id=organization.id,
            name="Default",
            slug="default",
            is_default=True,
            status="active",
        )
        db.add(workspace)
        db.flush()
        
        # Add user as organization owner
        member = OrganizationMember(
            id=uuid.uuid4(),
            organization_id=organization.id,
            user_id=user.id,
            workspace_id=workspace.id,
            role=UserRole.OWNER,
            is_active=True,
            joined_at=datetime.utcnow(),
        )
        db.add(member)
        db.commit()
        
        logger.info(f"User registered: {user.email}")
        
        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "org_id": str(organization.id)}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "org_id": str(organization.id)}
        )
        
        return {
            "user": user,
            "organization": organization,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    
    @staticmethod
    def login_user(db: Session, request: UserLoginRequest) -> dict:
        """
        Authenticate user and return tokens
        """
        user = db.query(User).filter(User.email == request.email).first()
        
        if not user or not verify_password(request.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        db.commit()
        
        # Get user's organization
        member = db.query(OrganizationMember).filter(
            OrganizationMember.user_id == user.id
        ).first()
        
        if not member:
            raise NotFoundException("User organization not found")
        
        logger.info(f"User logged in: {user.email}")
        
        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "org_id": str(member.organization_id)}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "org_id": str(member.organization_id)}
        )
        
        return {
            "user": user,
            "organization_id": member.organization_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    
    @staticmethod
    def verify_email(db: Session, user_id: uuid.UUID) -> User:
        """
        Mark email as verified
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found")
        
        user.is_email_verified = True
        user.email_verified_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Email verified for user: {user.email}")
        return user
