import asyncio
import uuid

from database.session import AsyncSessionLocal
from database.models import Tenant
from core.security import generate_api_key, hash_api_key


async def main():
    tenant_id = f"tenant_{uuid.uuid4().hex[:8]}"
    api_key = generate_api_key()

    tenant = Tenant(
        id=tenant_id,
        name="Default Tenant",
        api_key_hash=hash_api_key(api_key),
    )

    async with AsyncSessionLocal() as session:
        session.add(tenant)
        await session.commit()

    print("✅ Tenant created")
    print(f"Tenant ID: {tenant_id}")
    print(f"API Key (store securely): {api_key}")


if __name__ == "__main__":
    asyncio.run(main())
