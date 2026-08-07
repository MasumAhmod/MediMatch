from fastapi import APIRouter, HTTPException

from app.database.queries import (
    get_all_doctors,
    get_doctor_by_id,
    search_doctors,
    filter_doctors
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

# GET /api/v1/doctors/
# Get all doctors

@router.get("/")
def get_doctors():

    doctors = get_all_doctors()

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No active doctors found."
        )

    return {
        "doctors": doctors
    }


# GET /api/v1/doctors/search
# Search doctors

@router.get("/search")
def search_doctor(
    name: str | None = None,
    specialization: str | None = None
):

    doctors = search_doctors(
        name=name,
        specialization=specialization
    )

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No matching doctors found."
        )

    return {
        "doctors": doctors
    }

# GET /api/v1/doctors/filter
# Filter doctors

@router.get("/filter")
def filter_doctor(
    city: str | None = None,
    specialization: str | None = None,
    min_fee: float | None = None,
    max_fee: float | None = None,
    availability: str | None = None
):

    doctors = filter_doctors(
        city=city,
        specialization=specialization,
        min_fee=min_fee,
        max_fee=max_fee,
        availability=availability
    )

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No doctors found matching the filters."
        )

    return {
        "doctors": doctors
    }


# GET /api/v1/doctors/{doctor_id}
# Get doctor by ID

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int):

    doctor = get_doctor_by_id(doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    return {
        "doctor": doctor
    }