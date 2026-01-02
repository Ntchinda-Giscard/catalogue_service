from pydantic import BaseModel
from typing import List



class AttendeeSchema(BaseModel):
    name: str

class EventSchema(BaseModel):
    name: str
    attendees: List[AttendeeSchema]

