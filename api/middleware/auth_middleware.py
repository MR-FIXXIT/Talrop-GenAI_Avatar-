from fastapi import Header, HTTPException

class Tenant:
    def __init__(self, tenant_id: str):
        self.id = tenant_id

async def require_api_key(x_api_key: str = Header(...)):
    # TODO: lookup API key in DB or Redis
    if x_api_key != "dev-key":
        raise HTTPException(status_code=401, detail="Invalid API key")

    return Tenant(tenant_id="tenant_123")
