from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.routers.bookings import router as bookings_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Adizz Travel & Booking Management System",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "adizz-backend",
    }


app.include_router(bookings_router)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
)