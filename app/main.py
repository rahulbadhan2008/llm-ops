from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
import uvicorn

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "env": settings.APP_ENV}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
