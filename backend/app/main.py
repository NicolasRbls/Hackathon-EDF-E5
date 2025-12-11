from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .routers import devices, actions, stats, auth

# Auto-create tables (dev mode)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hackathon EDF Backend")

# CORS policy (Open permissions for Hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(actions.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
