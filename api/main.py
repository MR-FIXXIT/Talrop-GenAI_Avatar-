from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat, auth, health
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.tenant_context import TenantContextMiddleware

app = FastAPI(
    title="Avatar Chatbot API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(TenantContextMiddleware)
app.add_middleware(RateLimitMiddleware)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(health.router, prefix="/health", tags=["Health"])
