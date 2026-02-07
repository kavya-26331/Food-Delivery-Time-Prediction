import pandas as pd
import numpy as np
import joblib

# Load trained model and scaler
model = joblib.load("app/ml/model.pkl")
scaler = joblib.load("app/ml/scaler.pkl")

def predict_eta(distance_km, weather, hour_of_day, day_of_week, traffic_level, delivery_person_rating,
                multiple_deliveries, festival, prep_time_minutes, city_type, delivery_person_age, vehicle_condition):
    """
    Predict ETA using all available features
    """
    # Create feature vector in EXACT same order as training
    # Order: ['distance_km', 'hour_of_day', 'day_of_week', 'traffic_level', 'delivery_person_rating',
    #         'multiple_deliveries', 'festival', 'prep_time_minutes', 'delivery_person_age',
    #         'prep_time_traffic_level', 'distance_traffic_level', 'distance_multiple_deliveries',
    #         'weather_cloudy', 'weather_rainy', 'weather_snowy', 'weather_sunny',
    #         'city_type_rural', 'city_type_urban', 'vehicle_condition_average',
    #         'vehicle_condition_good', 'vehicle_condition_poor']

    # Calculate interaction features first
    prep_time_traffic_level = prep_time_minutes * traffic_level
    distance_traffic_level = distance_km * traffic_level
    distance_multiple_deliveries = distance_km * multiple_deliveries

    # Create DataFrame with features in exact training order
    features = {
        "distance_km": [distance_km],
        "hour_of_day": [hour_of_day],
        "day_of_week": [day_of_week],
        "traffic_level": [traffic_level],
        "delivery_person_rating": [delivery_person_rating],
        "multiple_deliveries": [multiple_deliveries],
        "festival": [festival],
        "prep_time_minutes": [prep_time_minutes],
        "delivery_person_age": [delivery_person_age],
        "prep_time_traffic_level": [prep_time_traffic_level],
        "distance_traffic_level": [distance_traffic_level],
        "distance_multiple_deliveries": [distance_multiple_deliveries],
        "weather_cloudy": [1 if weather == "cloudy" else 0],
        "weather_rainy": [1 if weather == "rainy" else 0],
        "weather_snowy": [1 if weather == "snowy" else 0],
        "weather_sunny": [1 if weather == "sunny" else 0],
        "city_type_rural": [1 if city_type == "rural" else 0],
        "city_type_urban": [1 if city_type == "urban" else 0],
        "vehicle_condition_average": [1 if vehicle_condition == "average" else 0],
        "vehicle_condition_good": [1 if vehicle_condition == "good" else 0],
        "vehicle_condition_poor": [1 if vehicle_condition == "poor" else 0]
    }

    X = pd.DataFrame(features)

    # Scale numerical features (same as training)
    numerical_features = ['distance_km', 'traffic_level', 'delivery_person_rating',
                         'multiple_deliveries', 'prep_time_minutes', 'delivery_person_age',
                         'prep_time_traffic_level', 'distance_traffic_level', 'distance_multiple_deliveries']

    X_scaled = X.copy()
    X_scaled[numerical_features] = scaler.transform(X[numerical_features])

    prediction = model.predict(X_scaled)[0]
    return prediction
