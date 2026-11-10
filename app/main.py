from fastapi import FastAPI

from app.database import Base, engine
from app.models import Visit
from app.routers import visits, explore


app = FastAPI(title="Travel Abroad API")

app.include_router(visits.router)
app.include_router(explore.router)


@app.get("/")
def root():
    return {"message": "Travel Abroad API. Docs: /docs"}