from sqlalchemy.orm import Session
from ..database.models import Bus, Station, Route, Schedule
from ..schemas.catalogue_schema import BusCreate, StationCreate, RouteCreate, ScheduleCreate

class CatalogueService:
    def __init__(self, db: Session):
        self.db = db

    # Stations
    def create_station(self, station: StationCreate):
        db_station = Station(name=station.name, city=station.city)
        self.db.add(db_station)
        self.db.commit()
        self.db.refresh(db_station)
        return db_station

    def get_stations(self):
        return self.db.query(Station).all()

    # Buses
    def create_bus(self, bus: BusCreate):
        db_bus = Bus(bus_number=bus.bus_number, capacity=bus.capacity, bus_type=bus.bus_type)
        self.db.add(db_bus)
        self.db.commit()
        self.db.refresh(db_bus)
        return db_bus

    # Routes
    def create_route(self, route: RouteCreate):
        db_route = Route(
            origin_id=route.origin_id,
            destination_id=route.destination_id,
            distance_km=route.distance_km
        )
        self.db.add(db_route)
        self.db.commit()
        self.db.refresh(db_route)
        return db_route

    # Schedules
    def create_schedule(self, schedule: ScheduleCreate):
        db_schedule = Schedule(
            route_id=schedule.route_id,
            bus_id=schedule.bus_id,
            departure_time=schedule.departure_time,
            arrival_time=schedule.arrival_time,
            price=schedule.price
        )
        self.db.add(db_schedule)
        self.db.commit()
        self.db.refresh(db_schedule)
        return db_schedule

    def search_schedules(self, origin_city: str, destination_city: str):
        # Find routes matching origin and destination cities
        routes = self.db.query(Route).join(
            Station, Route.origin_id == Station.id, aliased=True
        ).join(
            Station, Route.destination_id == Station.id, aliased=True
        ).filter(
            Route.origin.has(city=origin_city),
            Route.destination.has(city=destination_city)
        ).all()
        
        route_ids = [r.id for r in routes]
        
        # Get schedules for these routes
        schedules = self.db.query(Schedule).filter(Schedule.route_id.in_(route_ids)).all()
        return schedules
