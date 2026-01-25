from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

from core.config import settings

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, index=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def save_message(
    tenant_id: str,
    session_id: str,
    role: str,
    content: str
):
    async with AsyncSessionLocal() as session:
        msg = ChatMessage(
            id=f"{tenant_id}-{session_id}-{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            session_id=session_id,
            role=role,
            content=content
        )
        session.add(msg)
        await session.commit()
