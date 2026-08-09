from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# =========================================================
# API ROUTERS
# =========================================================

from app.api.health import router as health_router
from app.api.doctors import router as doctors_router
from app.api.prediction import router as prediction_router
from app.api.specializations import router as specializations_router

# =========================================================
# FRONTEND ROUTERS
# =========================================================

from app.routes.home import router as home_router
from app.routes.predict import router as predict_router
from app.routes.doctor import router as doctor_router


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="MediMatch API",
    description="AI-powered medical specialist and doctor recommendation API",
    version="1.0.0"
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# =========================================================
# API V1
# =========================================================

API_V1_PREFIX = "/api/v1"


# ---------------------------------------------------------
# Health API
# ---------------------------------------------------------

app.include_router(
    health_router,
    prefix=API_V1_PREFIX
)


# ---------------------------------------------------------
# Doctors API
# ---------------------------------------------------------

app.include_router(
    doctors_router,
    prefix=API_V1_PREFIX
)


# ---------------------------------------------------------
# Prediction API
# ---------------------------------------------------------

app.include_router(
    prediction_router
)


# ---------------------------------------------------------
# Specializations API
# ---------------------------------------------------------

app.include_router(
    specializations_router,
    prefix=API_V1_PREFIX
)


# =========================================================
# FRONTEND ROUTES
# =========================================================

# Home
app.include_router(
    home_router
)

# Symptoms / Result
app.include_router(
    predict_router
)

# Doctors / Doctor Profile
app.include_router(
    doctor_router
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to MediMatch",
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