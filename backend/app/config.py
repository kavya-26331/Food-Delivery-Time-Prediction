import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = "sqlite:///./food_delivery.db"
    GOOGLE_MAPS_API_KEY = "AIzaSyBy_zIde0RNzHFY77wor0A5_piauOS652k"
    WEATHER_API_KEY = "b2adae5a6211e55c98b2b922b388ce6e"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "llama3.1"
    MODEL_PATH = "./app/ml/model_utils.py"
