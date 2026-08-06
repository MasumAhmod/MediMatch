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


@router.get("/")
def get_doctors():
    """
    Retrieve all active doctors.
    """

    doctors = get_all_doctors()

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No active doctors found."
        )

    return {"doctors": doctors}


@router.get("/search")
def search_doctor(
    name: str | None = None,
    specialization: str | None = None
):
    """
    Search doctors by name or specialization.
    """

    doctors = search_doctors(
        name=name,
        specialization=specialization
    )

    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No matching doctors found."
        )

    return {"doctors": doctors}


@router.get("/filter")
def filter_doctor(
    city: str | None = None,
    specialization: str | None = None,
    min_fee: float | None = None,
    max_fee: float | None = None,
    availability: bool | None = None
):
    """
    Filter doctors.
    """

    doctors = filter_doctors(
        city=city,
        specialization=specialization,
        min_fee=min_fee,
        max_fee=max_fee,
        availability=availability
    )

    return {"doctors": doctors}


@router.get("/{doctor_id}")
def doctor_by_id(doctor_id: int):
    """
    Retrieve a doctor by ID.
    """

    doctor = get_doctor_by_id(doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    return {"doctor": doctor}