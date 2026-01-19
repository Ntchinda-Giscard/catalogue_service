from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .sessions import Base

class Station(Base):
    __tablename__ = "stations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    city: Mapped[str] = mapped_column(String, index=True)

class Bus(Base):
    __tablename__ = "buses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bus_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    capacity: Mapped[int] = mapped_column(Integer)
    bus_type: Mapped[str] = mapped_column(String) # AC, Non-AC, Sleeper

class Route(Base):
    __tablename__ = "routes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    origin_id: Mapped[int] = mapped_column(ForeignKey("stations.id"))
    destination_id: Mapped[int] = mapped_column(ForeignKey("stations.id"))
    distance_km: Mapped[float] = mapped_column(Float)
    
    origin = relationship("Station", foreign_keys=[origin_id])
    destination = relationship("Station", foreign_keys=[destination_id])

class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    bus_id: Mapped[int] = mapped_column(ForeignKey("buses.id"))
    departure_time: Mapped[str] = mapped_column(String) # ISO Format or Time string
    arrival_time: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)

    route = relationship("Route")
    bus = relationship("Bus")