from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas.events_schema import EventSchema
from ..services.events import EventsService, get_events_service
from typing import List


events_router = APIRouter(
    prefix="/api/v1/events",
    tags=["events"],
)

@events_router.get("/", response_model=List[EventSchema])
def get_events(service: EventsService = Depends(get_events_service)) -> List[EventSchema]:
    try:
        services = service.get_all_events()
        return services
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@events_router.post("/add", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
def create_event(event: EventSchema, service: EventsService = Depends(get_events_service)) -> EventSchema:
    try:
        new_event = service.create_event(event)
        return new_event
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@events_router.get("/{event_id}", response_model=EventSchema)
def get_event(event_id: int, service: EventsService = Depends(get_events_service)) -> EventSchema:
    try:
        event = service.get_event_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@events_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, service: EventsService = Depends(get_events_service)) -> None:
    try:
        success = service.delete_event(event_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))