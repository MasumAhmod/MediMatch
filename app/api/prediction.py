from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_disease
from app.ml.symptom_extractor import extract_symptoms

from app.utils.specialist import (
    get_specialization,
    get_specialization_keywords
)

from app.database.db import get_connection


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/v1/predict",
    tags=["Prediction"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class PredictionRequest(BaseModel):
    # Natural-language input
    text: str | None = None

    # Direct symptom list
    symptoms: list[str] | None = None


# =========================================================
# GET DOCTORS BY SPECIALIZATION
# =========================================================

def get_doctors_by_specialization(
    specialization: str
):
    """
    Returns active doctors matching a medical specialization.

    Doctors are sorted by consultation fee so that
    lower-cost doctors appear first.
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


# =========================================================
# POST /api/v1/predict/
# =========================================================

@router.post("/")
def predict(
    request: PredictionRequest
):
    """
    Predict disease from either:

    1. Natural-language text
    OR
    2. A list of symptoms.

    Then determine the recommended specialization
    and find matching doctors.
    """

    try:

        # =================================================
        # 1. VARIABLES
        # =================================================

        symptoms = []

        original_text = None

        input_type = None


        # =================================================
        # 2. NATURAL-LANGUAGE INPUT
        # =================================================

        if request.text and request.text.strip():

            original_text = request.text.strip()

            input_type = "natural_language"

            symptoms = extract_symptoms(
                original_text
            )


        # =================================================
        # 3. DIRECT SYMPTOM LIST
        # =================================================

        elif request.symptoms:

            input_type = "symptom_list"

            symptoms = [
                symptom.strip().lower()
                for symptom in request.symptoms
                if symptom and symptom.strip()
            ]


        # =================================================
        # 4. NO INPUT
        # =================================================

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Please provide symptoms or "
                    "describe your symptoms."
                )
            )


        # =================================================
        # 5. CHECK EXTRACTED SYMPTOMS
        # =================================================

        if not symptoms:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No recognizable symptoms were found. "
                    "Please describe your symptoms more clearly."
                )
            )


        # =================================================
        # 6. PREDICT DISEASE
        # =================================================

        disease = predict_disease(
            symptoms
        )

        if not disease:

            raise HTTPException(
                status_code=400,
                detail="Unable to predict disease."
            )


        # =================================================
        # 7. DETERMINE SPECIALIZATION
        # =================================================

        specialization = get_specialization(
            disease
        )

        if not specialization:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No specialization found for "
                    f"the predicted disease: {disease}"
                )
            )


        # =================================================
        # 8. FIND DOCTORS
        # =================================================

        doctors = get_doctors_by_specialization(
            specialization
        )


        # =================================================
        # 9. NATURAL-LANGUAGE DESCRIPTION
        # =================================================

        if len(symptoms) == 1:

            symptoms_text = symptoms[0]

        elif len(symptoms) == 2:

            symptoms_text = (
                f"{symptoms[0]} and {symptoms[1]}"
            )

        else:

            symptoms_text = (
                ", ".join(symptoms[:-1])
                + f", and {symptoms[-1]}"
            )


        prediction_message = (
            f"Based on the symptoms you described — "
            f"{symptoms_text} — our ML model predicts "
            f"{disease}."
        )


        # =================================================
        # 10. RETURN RESULT
        # =================================================

        return {

            # Original user input
            "input_text": original_text,

            # How prediction was made
            "input_type": input_type,

            # Extracted / selected symptoms
            "symptoms": symptoms,

            # Human-readable symptoms
            "symptoms_text": symptoms_text,

            # Prediction
            "disease": disease,

            # Natural-language message
            "prediction_message": prediction_message,

            # Recommended specialist
            "specialization": specialization,

            # Recommended doctors
            "doctors": doctors
        }


    # =====================================================
    # HTTP EXCEPTIONS
    # =====================================================

    except HTTPException:
        raise


    # =====================================================
    # UNEXPECTED ERROR
    # =====================================================

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )