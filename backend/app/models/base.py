# Base Model with Common Fields

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import DateTime, func, UUID
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    """
    Base class for all models
    """
    pass

class BaseModel(Base):
    """
    Base model with common fields
    """
    __abstract__ = True
    
    id: uuid.UUID = declared_attr(lambda: BaseModel.__id_column__())
    created_at: datetime = declared_attr(lambda: BaseModel.__created_at_column__())
    updated_at: datetime = declared_attr(lambda: BaseModel.__updated_at_column__())
    deleted_at: datetime = declared_attr(lambda: BaseModel.__deleted_at_column__())
    
    @staticmethod
    def __id_column__():
        from sqlalchemy import Column
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    
    @staticmethod
    def __created_at_column__():
        return DateTime(timezone=True, default=func.now(), nullable=False)
    
    @staticmethod
    def __updated_at_column__():
        return DateTime(timezone=True, default=func.now(), onupdate=func.now(), nullable=False)
    
    @staticmethod
    def __deleted_at_column__():
        return DateTime(timezone=True, nullable=True)
