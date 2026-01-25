from fastapi import APIRouter, HTTPException
from api.schemas.tenant import TenantCreate, TenantResponse
from core.security import generate_api_key

router = APIRouter()

@router.post("/create", response_model=TenantResponse)
async def create_tenant(payload: TenantCreate):
    """
    Creates a new tenant (admin-only in real systems)
    """
    api_key = generate_api_key()

    # TODO: save tenant to DB
    return TenantResponse(
        tenant_id="tenant_123",
        api_key=api_key
    )
