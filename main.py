from fastapi import FastAPI
from database.models import Base
from src.routes.event_route import events_router
from src.database.sessions import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Incude middleware, CORS, etc. if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(events_router)

@app.get("/health")
def read_root():
    return {"API": "Healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)