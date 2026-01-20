from fastapi import FastAPI
from .database.sessions import engine, Base
from .routes import catalogue_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bus Booking - Catalogue Service",
    description="Service for managing Stations, Buses, Routes, and Schedules",
    version="1.0.0"
)

app.include_router(catalogue_routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CatalogueService"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)