from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import devices

# Create tables automatically on startup
try:
    models.Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")
except Exception as e:
    print(f"Error creating database: {e}")

app = FastAPI(title="EDF Hackathon Tracker")

app.include_router(devices.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
