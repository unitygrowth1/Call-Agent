# FastAPI Backend Configuration

import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application configuration
    """
    
    # Application
    APP_NAME: str = "Call Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/call_agent"
    )
    DB_ECHO: bool = DEBUG
    DB_POOL_SIZE: int = 20
    DB_POOL_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # JWT & Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # AI/ML Services
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    
    # Speech Services
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    PIPER_DATA_DIR: str = os.getenv("PIPER_DATA_DIR", "/app/data/piper")
    
    # Telephony
    ASTERISK_HOST: str = os.getenv("ASTERISK_HOST", "localhost")
    ASTERISK_PORT: int = int(os.getenv("ASTERISK_PORT", "5060"))
    ASTERISK_USER: str = os.getenv("ASTERISK_USER", "admin")
    ASTERISK_PASSWORD: str = os.getenv("ASTERISK_PASSWORD", "admin")
    WEBRTC_STUN_SERVERS: list = [
        "stun:stun.l.google.com:19302",
        "stun:stun1.l.google.com:19302",
    ]
    
    # Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@callagent.com")
    SMTP_USE_TLS: bool = True
    
    # WhatsApp
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_ACCESS_TOKEN: Optional[str] = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_WEBHOOK_VERIFY_TOKEN: Optional[str] = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN")
    
    # SMS (Twilio)
    SMS_PROVIDER: str = os.getenv("SMS_PROVIDER", "twilio")
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER")
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_CALLBACK_URL: str = os.getenv("GOOGLE_CALLBACK_URL", "http://localhost:8000/auth/google/callback")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Files & Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = ["pdf", "docx", "txt", "csv", "xlsx"]
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379")
    
    # AWS (Optional)
    AWS_REGION: Optional[str] = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = os.getenv("AWS_S3_BUCKET")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
