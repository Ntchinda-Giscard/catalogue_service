from pydantic import BaseModel
from typing import List, Optional

class StationBase(BaseModel):
    name: str
    city: str

class StationCreate(StationBase):
    pass

class StationResponse(StationBase):
    id: int
    class Config:
        from_attributes = True

class BusBase(BaseModel):
    bus_number: str
    capacity: int
    bus_type: str

class BusCreate(BusBase):
    pass

class BusResponse(BusBase):
    id: int
    class Config:
        from_attributes = True

class RouteBase(BaseModel):
    origin_id: int
    destination_id: int
    distance_km: float

class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int
    origin: StationResponse
    destination: StationResponse
    class Config:
        from_attributes = True

class ScheduleBase(BaseModel):
    route_id: int
    bus_id: int
    departure_time: str
    arrival_time: str
    price: float

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    route: RouteResponse
    bus: BusResponse
    class Config:
        from_attributes = True
