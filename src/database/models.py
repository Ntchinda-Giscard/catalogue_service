from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship



class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    attendees: Mapped[List[Attendee]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

class Attendee(Base):
    __tablename__ = "attendees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped[Event] = relationship(back_populates="attendees")