from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    return {
        "application": "MediMatch",
        "status": "Healthy",
        "version": "1.0.0"
    }