from fastapi import APIRouter, HTTPException

from app.database.queries import (
    get_all_specializations,
    search_specializations
)

router = APIRouter(
    prefix="/specializations",
    tags=["Specializations"]
)


# GET /specializations
@router.get("/")
def get_specializations():
    """
    Get all available specializations.
    """

    specializations = get_all_specializations()

    if not specializations:
        raise HTTPException(
            status_code=404,
            detail="No specializations found."
        )

    return {
        "specializations": specializations
    }


# GET /specializations/search
# /specializations/search?name=Cardiology

@router.get("/search")
def search_specialization(name: str):
    """
    Return all doctors of a specialization.
    """

    doctors = search_specializations(name)

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No doctors found."
        )

    return {
        "specialization": name,
        "total_doctors": len(doctors),
        "doctors": doctors
    }