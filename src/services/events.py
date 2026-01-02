from ..schemas.events_schema import EventSchema
from typing import List


class EventsService:

    def __init__(self):
        self.events: List[EventSchema]