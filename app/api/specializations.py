from fastapi import APIRouter, HTTPException

from app.database.queries import (
    get_all_specializations,
    search_specializations
)


router = APIRouter(
    prefix="/specializations",
    tags=["Specializations"]
)


# GET /api/v1/specializations

@router.get("/")
def get_specializations():

    specializations = get_all_specializations()

    if not specializations:
        raise HTTPException(
            status_code=404,
            detail="No specializations found."
        )

    return {
        "specializations": specializations
    }


# GET /api/v1/specializations/search

@router.get("/search")
def search_specialization(
    name: str
):

    specializations = search_specializations(
        name
    )

    if not specializations:
        raise HTTPException(
            status_code=404,
            detail="No matching specialization found."
        )

    return {
        "specializations": specializations
    }