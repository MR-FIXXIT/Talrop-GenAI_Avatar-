from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Index,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    api_key_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


Index(
    "idx_tenant_session",
    ChatMessage.tenant_id,
    ChatMessage.session_id,
)
