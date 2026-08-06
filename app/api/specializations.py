from fastapi import APIRouter, HTTPException

from fastapi import APIRouter, HTTPException

from app.database.queries import (
    get_all_specializations,
    get_specialization_by_id,
    search_specializations
)

router = APIRouter(
    prefix="/specializations",
    tags=["Specializations"]
)


# GET /specializations
# Get all active specializations
@router.get("/")
def get_specializations():

    specializations = get_all_specializations()

    if not specializations:
        raise HTTPException(
            status_code=404,
            detail="No specializations found."
        )

    return {"specializations": specializations}


# GET /specializations/search
# Search specialization by name
@router.get("/search")
def search_specialization(name: str):

    specializations = search_specializations(name)

    if not specializations:
        raise HTTPException(
            status_code=404,
            detail="No matching specialization found."
        )

    return {"specializations": specializations}

# GET /specializations/{id}
# Get specialization by ID
@router.get("/{id}")
def get_specialization(id: int):

    specialization = get_specialization_by_id(id)

    if specialization is None:
        raise HTTPException(
            status_code=404,
            detail="Specialization not found."
        )

    return {"specialization": specialization}