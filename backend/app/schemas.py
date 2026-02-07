from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class DeliveryCreate(BaseModel):
    restaurant_lat: float
    restaurant_lng: float
    customer_lat: float
    customer_lng: float
    weather: str

class DeliveryResponse(BaseModel):
    id: int
    restaurant_lat: float
    restaurant_lng: float
    customer_lat: float
    customer_lng: float
    distance_km: float
    weather: str
    eta_minutes: float

class ETAPredict(BaseModel):
    distance_km: float
    weather: str
    hour_of_day: int
    day_of_week: int
    traffic_level: float
    delivery_person_rating: float
    multiple_deliveries: int
    festival: bool
    prep_time_minutes: float
    city_type: str
    delivery_person_age: int
    vehicle_condition: str

class ETAResponse(BaseModel):
    eta_minutes: float

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# User schemas
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Restaurant schemas
class RestaurantCreate(BaseModel):
    name: str
    lat: float
    lng: float

class RestaurantResponse(BaseModel):
    id: int
    name: str
    lat: float
    lng: float

# Order schemas
class OrderCreate(BaseModel):
    restaurant_id: int
    items: str  # JSON string

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    restaurant_id: int
    rider_id: Optional[int]
    status: str
    created_at: datetime
    items: str

class OrderStatus(BaseModel):
    status: str

class TrackOrderRequest(BaseModel):
    order_number: str
    restaurant_id: int

class ContactInfo(BaseModel):
    email: str = "support@fooddelivery.com"
    phone: str = "1-800-123-4567"
    address: str = "123 Food St, City, State 12345"

# Location tracking schemas
class LocationUpdate(BaseModel):
    order_id: int
    lat: float
    lng: float
    timestamp: Optional[datetime] = None

class LocationResponse(BaseModel):
    order_id: int
    lat: float
    lng: float
    timestamp: datetime
    status: str

# Rider schemas
class RiderCreate(BaseModel):
    email: str
    password: str
    name: str

class RiderResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

class RiderLoginRequest(BaseModel):
    email: str
    password: str

class RiderTokenResponse(BaseModel):
    access_token: str
    token_type: str

# Assign Rider schema
class AssignRider(BaseModel):
    rider_id: int
