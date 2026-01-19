#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    '''
    Enum for the different means of communication
    '''
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    '''
    Class that represent an alien contact
    '''
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_model(self):
        error = ""
        condition1 = not self.is_verified
        condition2 = self.witness_count < 3

        if len(self.contact_id) < 2 or self.contact_id[:2] != "AC":
            error = "Contact ID must start with 'AC' (Alien Contact)"
        elif self.contact_type == ContactType.physical and condition1:
            error = "physical contact reports must be verified"
        elif self.contact_type == ContactType.telepathic and condition2:
            error = "telepathic contact requires at least 3 witnesses"
        elif self.signal_strength > 7 and self.message_received is None:
            error = "Strong signals (> 7.0) should include received messages"

        if error != "":
            raise ValueError(error)

        return self


def convert_duration(duration: int) -> str:
    '''
    Convert a minutes duration into an hour and minutes duration
    '''
    res = ""
    if duration >= 60:
        plurial = ""
        if duration >= 120:
            plurial = "s"
        res += f"{duration // 60} hour{plurial}"
        if duration % 60 != 0:
            res += " "
    if duration % 60 == 0:
        return res

    plurial = ""
    if duration % 60 != 1:
        plurial = "s"
    res += f"{duration % 60} minute{plurial}"

    return res


def display_contact(contact: AlienContact) -> None:
    '''
    Display the alien contact informations
    '''
    print("ID:", contact.contact_id)
    print("Type:", contact.contact_type)
    print("Location:", contact.location)
    print(f"Signal: {round(contact.signal_strength, 1)}/10")
    print("Duration:", convert_duration(contact.duration_minutes))
    print("Witness:", contact.witness_count)
    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")


def main() -> None:
    '''
    Test the class
    '''
    print("========================================")
    try:
        alien_contact1 = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.radio,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        print("Valid contact report:")
        display_contact(alien_contact1)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"][13:])
    print()

    try:
        print("========================================")
        alien_contact2 = AlienContact(
            contact_id="AC_2471_PEP",
            contact_type=ContactType.telepathic,
            location="Area 42, Lyon",
            signal_strength=4.2,
            duration_minutes=42,
            witness_count=1,
            message_received="Greetings from CRAPPO the First"
        )
        print("Valid contact report:")
        display_contact(alien_contact2)
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"][13:])


if __name__ == "__main__":
    print("Alien Contact Log Validation")

    main()
