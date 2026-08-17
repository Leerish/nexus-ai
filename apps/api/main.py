from fastapi import FastAPI
from apps.api.routes.investigations import router as investigations_router


app = FastAPI(
    title="Nexus AI",
    description="Enterprise Cognitive Intelligence Platform",
    version="0.1.0",
)

app.include_router(investigations_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "Nexus AI",
        "version": "0.1.0",
    }