from fastapi import APIRouter
from app.schemas import ETAPredict, ETAResponse
from app.services.eta_predictor import predict_eta
import numpy as np

router = APIRouter()

@router.post("/eta", response_model=ETAResponse)
def predict_eta_endpoint(request: ETAPredict):

    # Get prediction using user-provided inputs
    eta = predict_eta(
        request.distance_km,
        request.weather,
        request.hour_of_day,
        request.day_of_week,
        request.traffic_level,
        request.delivery_person_rating,
        request.multiple_deliveries,
        request.festival,
        request.prep_time_minutes,
        request.city_type,
        request.delivery_person_age,
        request.vehicle_condition
    )

    # Convert numpy float to regular Python float
    if isinstance(eta, np.floating):
        eta = float(eta)
    elif hasattr(eta, 'item'):
        eta = eta.item()

    return {"eta_minutes": eta}
