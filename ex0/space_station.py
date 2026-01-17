#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime = Field(default_factory=lambda: datetime.now())
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    '''
    Display the space station informations
    '''
    print("ID:", station.station_id)
    print("Name:", station.name)
    print("Crew:", station.crew_size)
    print("Power:", station.power_level)
    print("Oxygen:", station.oxygen_level)
    print(f"Status: {'Non ' if station.is_operational else ''}Operational")


def main() -> None:
    '''
    Test the class
    '''
    print("========================================")
    try:
        space_station1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=True
        )
        print("Valid station created:")
        display_station(space_station1)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])
    print()

    try:
        print("========================================")
        space_station2 = SpaceStation(
            station_id="100SSI",
            name="Station Space International",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=False
        )
        print("Valid station created:")
        display_station(space_station2)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    print("Space Station Data Validation")

    main()
