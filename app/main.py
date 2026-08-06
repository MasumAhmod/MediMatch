from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.doctors import router as doctors_router
from app.api.prediction import router as prediction_router
from app.api.specializations import router as specializations_router

app = FastAPI(
    title="MediMatch API",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(doctors_router)
app.include_router(prediction_router)
app.include_router(specializations_router)