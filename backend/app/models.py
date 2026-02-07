from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime



class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_lat = Column(Float)
    restaurant_lng = Column(Float)
    customer_lat = Column(Float)
    customer_lng = Column(Float)
    distance_km = Column(Float)
    weather = Column(String)
    eta_minutes = Column(Float)
