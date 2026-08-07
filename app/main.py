from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.doctors import router as doctors_router
from app.api.prediction import router as prediction_router
from app.api.specializations import router as specializations_router


app = FastAPI(
    title="MediMatch API",
    description="AI-powered medical specialist and doctor recommendation API",
    version="1.0.0"
)


# =========================================================
# API V1 ROUTERS
# =========================================================

API_V1_PREFIX = "/api/v1"


app.include_router(
    health_router,
    prefix=API_V1_PREFIX
)

app.include_router(
    doctors_router,
    prefix=API_V1_PREFIX
)

app.include_router(
    prediction_router
)

app.include_router(
    specializations_router,
    prefix=API_V1_PREFIX
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to MediMatch API",
        "version": "1.0.0",
        "api": "/api/v1",
        "docs": "/docs"
    }


# =========================================================
# API V1 ROOT
# =========================================================

@app.get("/api/v1/")
def api_v1_root():

    return {
        "message": "Welcome to MediMatch API v1",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health/",
            "doctors": "/api/v1/doctors/",
            "specializations": "/api/v1/specializations/",
            "prediction": "/api/v1/predict/"
        },
        "docs": "/docs"
    }