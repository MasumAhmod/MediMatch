from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_disease

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    symptoms: list[str]


@router.post("/")
def predict(request: PredictionRequest):
    """
    Predict disease from symptom names.
    """

    try:
        disease = predict_disease(request.symptoms)

        return {
            "disease": disease
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )