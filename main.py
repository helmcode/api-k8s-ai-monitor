from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api import router
from config.db import Base, engine

# Models
from models.incidents import Incident
from models.incident_notifications import IncidentNotification

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="K8s AI Monitor API",
    description="""
    API for monitoring kubernetes clusters.
    """,
    version="0.0.1-alpha"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
