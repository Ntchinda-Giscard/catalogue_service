from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.sessions import get_db
from ..services.catalogue_service import CatalogueService
from ..schemas.catalogue_schema import (
    StationCreate, StationResponse,
    BusCreate, BusResponse,
    RouteCreate, RouteResponse,
    ScheduleCreate, ScheduleResponse
)

router = APIRouter(
    prefix="/catalogue",
    tags=["catalogue"]
)

def get_service(db: Session = Depends(get_db)) -> CatalogueService:
    return CatalogueService(db)

@router.post("/stations", response_model=StationResponse)
def create_station(station: StationCreate, service: CatalogueService = Depends(get_service)):
    return service.create_station(station)

@router.get("/stations", response_model=List[StationResponse])
def get_stations(service: CatalogueService = Depends(get_service)):
    return service.get_stations()

@router.post("/buses", response_model=BusResponse)
def create_bus(bus: BusCreate, service: CatalogueService = Depends(get_service)):
    return service.create_bus(bus)

@router.post("/routes", response_model=RouteResponse)
def create_route(route: RouteCreate, service: CatalogueService = Depends(get_service)):
    return service.create_route(route)

@router.get("/routes/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, service: CatalogueService = Depends(get_service)):
    route = service.get_route(route_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return route

@router.post("/schedules", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, service: CatalogueService = Depends(get_service)):
    return service.create_schedule(schedule)

@router.get("/search", response_model=List[ScheduleResponse])
def search_buses(
    origin: str, 
    destination: str, 
    service: CatalogueService = Depends(get_service)
):
    """
        Search for bus schedules between two cities.
    """
    return service.search_schedules(origin, destination)
