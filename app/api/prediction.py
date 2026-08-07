from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_disease
from app.utils.specialist import get_specialization


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    symptoms: list[str]


@router.post("/")
def predict(request: PredictionRequest):
    """
    Predict disease and recommended medical specialization.
    """

    if not request.symptoms:
        raise HTTPException(
            status_code=400,
            detail="At least one symptom is required."
        )

    try:
        disease = predict_disease(request.symptoms)

        specialization = get_specialization(disease)

        return {
            "disease": disease,
            "specialization": specialization
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )