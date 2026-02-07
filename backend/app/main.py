from fastapi import FastAPI
from app.routers.predict import router as predict_router
from app.routers.rag_api import router as rag_router
from app.routers.rider_ai import router as rider_router

from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(predict_router, prefix="/predict", tags=["predict"])
app.include_router(rag_router, prefix="/rag", tags=["rag"])
app.include_router(rider_router, prefix="/ai", tags=["ai"])


@app.get("/")
def read_root():
    return {"message": "Food Delivery API"}
