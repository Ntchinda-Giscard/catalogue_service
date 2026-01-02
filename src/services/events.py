from ..schemas.events_schema import EventSchema
from typing import List
from fastapi import Depends
from ..database.sessions import get_db
from sqlalchemy.orm import Session
from ..database.models import Event, Attendee

class EventsService:

    def __init__(self):
        self.events: List[EventSchema]

    def get_all_events(self, db: Session = Depends(get_db)) -> List[EventSchema]:
        events = db.query(Event).all()
        self.events = [EventSchema.from_orm(event) for event in events]

        return self.events
    
    def create_event(self, event_data: EventSchema, db: Session = Depends(get_db)) -> EventSchema:
        new_event = Event(name=event_data.name)
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        for attendee in event_data.attendees:
            new_attendee = Attendee(name=attendee.name, event_id=new_event.id)
            db.add(new_attendee)

        db.commit()
        db.refresh(new_event)

        return EventSchema.from_orm(new_event)
    
    def get_event_by_id(self, event_id: int, db: Session = Depends(get_db)) -> EventSchema | None:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event:
            return EventSchema.from_orm(event)
        return None
    
    def delete_event(self, event_id: int, db: Session = Depends(get_db)) -> bool:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event:
            db.delete(event)
            db.commit()
            return True
        return False