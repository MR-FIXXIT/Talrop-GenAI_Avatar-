from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str

class TenantResponse(BaseModel):
    tenant_id: str
    api_key: str
