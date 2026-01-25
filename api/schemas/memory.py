from pydantic import BaseModel
from typing import List

class MemoryItem(BaseModel):
    role: str
    content: str

class ConversationMemory(BaseModel):
    session_id: str
    history: List[MemoryItem]
