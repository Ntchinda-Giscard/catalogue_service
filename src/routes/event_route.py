from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas.events_schema import EventSchema
from ..services.events import EventsService
from typing import List


events_router = APIRouter(
    prefix="api/v1/events",
    tags=["events"],
)

@events_router.get("/", response_model=List[EventSchema])
def get_events(service: EventsService = Depends()) -> List[EventSchema]:
    try:
        services = service.get_all_events()
        return services
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@events_router.post("/add", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
def create_event(event: EventSchema, service: EventsService = Depends()) -> EventSchema:
    try:
        new_event = service.create_event(event)
        return new_event
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))