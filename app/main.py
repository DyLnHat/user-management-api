from fastapi import FastAPI

from app.api.v1 import router

app = FastAPI(
    title="User Management API",
    description="REST API for user management with roles and JWT authentication",
    version="1.0.0",
)

app.include_router(router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}