#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
from typing import List


class Rank(str, Enum):
    '''
    Enum for the different possible rank in the crew
    '''
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    '''
    Class that represent a person in the crew
    '''
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


def not_min_rank(crew: List[CrewMember]) -> bool:
    '''
    Return True if there are no Commander or Captain in the crew, else False
    '''
    nb_commander, nb_captain = 0, 0
    for person in crew:
        if person.rank == Rank.commander:
            nb_commander += 1
        elif person.rank == Rank.captain:
            nb_captain += 1

    return nb_commander == 0 and nb_captain == 0


def active_crew(crew: List[CrewMember]) -> bool:
    '''
    Return True if all the crew is active, else False
    '''
    for person in crew:
        if not person.is_active:
            return False
    return True


def experience_crew(crew: List[CrewMember]) -> bool:
    '''
    Return True if all the crew is experience
    '''
    nb_experience = 0
    for person in crew:
        if person.years_experience > 5:
            nb_experience += 1
    return nb_experience >= len(crew) / 2


class SpaceMission(BaseModel):
    '''
    Class that represent a space misson
    '''
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    lauch_date: datetime = Field(default_factory=lambda: datetime.now())
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode="after")
    def check_model(self):
        error = ""

        if len(self.mission_id) == 0 or self.mission_id[0] != "M":
            error = "Mission ID must start with 'M'"
        elif not_min_rank(self.crew):
            error = "Must have at least one Commander or Captain"
        elif self.duration_days > 365 and not experience_crew(self.crew):
            error = "Long missions (> 365 days) "
            error += "need 50% experienced crew (5+ years)"
        elif not active_crew(self.crew):
            error = "All crew members must be active"

        if error != "":
            raise ValueError(error)

        return self


def display_mission(mission: SpaceMission) -> None:
    '''
    Display the space mission informations
    '''
    print("Mission:", mission.mission_name)
    print("ID:", mission.mission_id)
    print("Destination:", mission.destination)
    plurial = "s" if mission.duration_days > 1 else ""
    print(f"Duration: {mission.duration_days} day{plurial}")
    print(f"Budget: ${round(mission.budget_millions, 2)}M")
    print("Crew size:", len(mission.crew))

    print("Crew members:")
    for person in mission.crew:
        print(f"- {person.name} ({person.rank}) - {person.specialization}")


def main() -> None:
    '''
    Test the class
    '''
    print("========================================")
    try:
        space_mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="Person005",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    specialization="Mission Command",
                    age=37,
                    years_experience=5
                ),
                CrewMember(
                    member_id="Person006",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    specialization="Navigation",
                    age=63,
                    years_experience=17
                ),
                CrewMember(
                    member_id="Person007",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    specialization="Engineering",
                    age=58,
                    years_experience=20
                )
            ]
        )
        print("Valid mission created:")
        display_mission(space_mission1)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"][13:])
    print()

    try:
        print("========================================")
        space_mission2 = SpaceMission(
            mission_id="M2026_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="Person005",
                    name="Sarah Connor",
                    rank=Rank.cadet,
                    specialization="Mission Command",
                    age=37,
                    years_experience=5
                ),
                CrewMember(
                    member_id="Person006",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    specialization="Navigation",
                    age=63,
                    years_experience=17
                ),
                CrewMember(
                    member_id="Person007",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    specialization="Engineering",
                    age=58,
                    years_experience=21
                )
            ]
        )
        print("Valid mission created:")
        display_mission(space_mission2)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"][13:])


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    main()
