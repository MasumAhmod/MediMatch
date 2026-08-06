from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ml.predictor import predict_disease

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    symptoms: list[int]


@router.post("/")
def predict(request: PredictionRequest):
    """
    Predict disease from symptoms.
    """

    result = predict_disease(request.symptoms)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Prediction failed."
        )

    return {
        "disease": result
    }