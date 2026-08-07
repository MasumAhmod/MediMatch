from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_disease
from app.utils.specialist import (
    get_specialization,
    get_specialization_keywords
)
from app.database.db import get_connection


# ROUTER

router = APIRouter(
    prefix="/api/v1/predict",
    tags=["Prediction"]
)


# REQUEST MODEL

class PredictionRequest(BaseModel):
    symptoms: list[str]


# GET DOCTORS BY SPECIALIZATION

def get_doctors_by_specialization(
    specialization: str
):
    """
    Returns doctors matching a medical specialization.

    The doctors table contains detailed specialization
    names, so keyword-based matching is used.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:

        keywords = get_specialization_keywords(
            specialization
        )

        if not keywords:
            return []

        with connection.cursor() as cursor:

            conditions = []
            params = []

            for keyword in keywords:

                conditions.append(
                    "LOWER(specialization) LIKE %s"
                )

                params.append(
                    f"%{keyword.lower()}%"
                )

            where_clause = " OR ".join(
                conditions
            )

            sql = f"""
                SELECT
                    doctor_id,
                    doctor_name,
                    degree,
                    specialization,
                    designation,
                    current_workplace,
                    chamber_hospital,
                    city,
                    visiting_hours,
                    appointment_phone,
                    appointment_fee,
                    availability,
                    is_active,
                    created_at,
                    updated_at
                FROM doctors
                WHERE is_active = 1
                AND ({where_clause})
                ORDER BY appointment_fee ASC
            """

            cursor.execute(
                sql,
                tuple(params)
            )

            return cursor.fetchall()

    finally:
        connection.close()


# POST /api/v1/predict/

@router.post("/")
def predict(
    request: PredictionRequest
):
    """
    Predict disease, determine medical specialization,
    and return matching doctors.
    """

    # Validate symptoms

    if not request.symptoms:

        raise HTTPException(
            status_code=400,
            detail="At least one symptom is required."
        )

    try:

        # 1. Predict disease

        disease = predict_disease(
            request.symptoms
        )

        if not disease:

            raise HTTPException(
                status_code=400,
                detail="Unable to predict disease."
            )

        # 2. Determine specialization

        specialization = get_specialization(
            disease
        )

        if not specialization:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No specialization found for "
                    "the predicted disease."
                )
            )

        # 3. Find doctors

        doctors = get_doctors_by_specialization(
            specialization
        )

        # 4. Return result

        return {
            "disease": disease,
            "specialization": specialization,
            "doctors": doctors
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )