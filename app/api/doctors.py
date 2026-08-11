from fastapi import APIRouter, HTTPException

from app.database.queries import (
    get_all_doctors,
    get_doctor_by_id,
    search_doctors,
    filter_doctors,
    get_doctors_by_specialization
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# =========================================================
# GET ALL DOCTORS
# =========================================================
# GET /api/v1/doctors/

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


# =========================================================
# SEARCH DOCTORS
# =========================================================
# GET /api/v1/doctors/search

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


# =========================================================
# FILTER DOCTORS
# =========================================================
# GET /api/v1/doctors/filter

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


# =========================================================
# GET DOCTORS BY SPECIALIZATION
# =========================================================
#
# Example:
#
# /api/v1/doctors/specialization?specialization=Urology
#
# =========================================================

@router.get("/specialization")
def doctors_by_specialization(
    specialization: str
):

    if not specialization.strip():

        raise HTTPException(
            status_code=400,
            detail="Specialization is required."
        )


    doctors = get_doctors_by_specialization(
        specialization.strip()
    )


    if not doctors:

        raise HTTPException(
            status_code=404,
            detail=(
                "No doctors found for specialization: "
                + specialization
            )
        )


    return {
        "specialization": specialization,
        "doctors": doctors
    }


# =========================================================
# GET DOCTOR BY ID
# =========================================================
#
# IMPORTANT:
# This must remain AFTER /specialization.
#
# =========================================================

@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int
):

    doctor = get_doctor_by_id(
        doctor_id
    )


    if doctor is None:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )


    return {
        "doctor": doctor
    }