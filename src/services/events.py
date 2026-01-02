from ..schemas.events_schema import EventSchema
from typing import List
from fastapi import Depends
from ..database.sessions import get_db
from sqlalchemy.orm import Session
from ..database.models import Event, Attendee

class EventsService:

    def __init__(self, db: Session):
        self.db = db
        self.events: List[EventSchema] = []

    def get_all_events(self) -> List[EventSchema]:
        events = self.db.query(Event).all()
        self.events = [EventSchema.from_orm(event) for event in events]
        return self.events
    
    def create_event(self, event_data: EventSchema) -> EventSchema:
        new_event = Event(name=event_data.name)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)

        for attendee in event_data.attendees:
            new_attendee = Attendee(name=attendee.name, event_id=new_event.id)
            self.db.add(new_attendee)

        self.db.commit()
        self.db.refresh(new_event)

        return EventSchema.from_orm(new_event)
    
    def get_event_by_id(self, event_id: int) -> EventSchema | None:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if event:
            return EventSchema.from_orm(event)
        return None
    
    def delete_event(self, event_id: int) -> bool:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False


def get_events_service(db: Session = Depends(get_db)) -> EventsService:
    return EventsService(db)