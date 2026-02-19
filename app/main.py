from fastapi import FastAPI
from app.database import engine, Base
from app.models import user
from app.routers import user as user_router

app = FastAPI(title="LicitaPro API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)

@app.get("/")
def home():
    return {"message": "Welcome to LicitaPro API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
