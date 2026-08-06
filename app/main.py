from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.doctors import router as doctors_router
from app.api.prediction import router as prediction_router
from app.api.specializations import router as specializations_router

app = FastAPI(
    title="MediMatch API",
    version="1.0.0"
)

API_PREFIX = "/api/v1"

app.include_router(health_router, prefix=API_PREFIX)
app.include_router(doctors_router, prefix=API_PREFIX)
app.include_router(prediction_router, prefix=API_PREFIX)
app.include_router(specializations_router, prefix=API_PREFIX)