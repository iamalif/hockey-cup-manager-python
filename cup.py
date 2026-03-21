# cup.py
# Defines the Cup class, which holds metadata about the hockey cup event
# (name, location, dates, etc.). A single Cup instance is shared across
# the application and can be viewed and edited through the UI.


class Cup:
    """
    Represents the hockey cup event itself.

    Attributes (private):
        __name        : name of the cup
        __location    : city / venue where the event takes place
        __sport_type  : type of sport (e.g. 'Ice Hockey')
        __start_date  : start date of the event (YYYY-MM-DD)
        __end_date    : end date of the event (YYYY-MM-DD)
        __description : free-text description of the cup

    Collaborations:
        - Used by UI to display and edit cup information.
        - Stored/loaded by TeamStorage as part of the main data file.
    """

    def __init__(
        self,
        name: str = "Hockey Cup",
        location: str = "Stockholm",
        sport_type: str = "Ice Hockey",
        start_date: str = "",
        end_date: str = "",
        description: str = "",
    ):
        """
        Initialise the Cup with event details.

        Args:
            name        : name of the cup event
            location    : city/venue for the event
            sport_type  : type of sport
            start_date  : start date (YYYY-MM-DD)
            end_date    : end date (YYYY-MM-DD)
            description : short description of the event
        """
        self.__name = name
        self.__location = location
        self.__sport_type = sport_type
        self.__start_date = start_date
        self.__end_date = end_date
        self.__description = description

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    def get_name(self) -> str:
        """Return the cup name."""
        return self.__name

    def get_location(self) -> str:
        """Return the city or venue where the event takes place."""
        return self.__location

    def get_sport_type(self) -> str:
        """Return the type of sport (e.g. 'Ice Hockey')."""
        return self.__sport_type

    def get_start_date(self) -> str:
        """Return the start date of the event (YYYY-MM-DD)."""
        return self.__start_date

    def get_end_date(self) -> str:
        """Return the end date of the event (YYYY-MM-DD)."""
        return self.__end_date

    def get_description(self) -> str:
        """Return the free-text description of the cup."""
        return self.__description

    # ------------------------------------------------------------------ #
    # Setters
    # ------------------------------------------------------------------ #

    def set_name(self, name: str) -> None:
        """Update the cup name."""
        self.__name = name

    def set_location(self, location: str) -> None:
        """Update the city or venue."""
        self.__location = location

    def set_sport_type(self, sport_type: str) -> None:
        """Update the sport type."""
        self.__sport_type = sport_type

    def set_start_date(self, start_date: str) -> None:
        """Update the start date (YYYY-MM-DD)."""
        self.__start_date = start_date

    def set_end_date(self, end_date: str) -> None:
        """Update the end date (YYYY-MM-DD)."""
        self.__end_date = end_date

    def set_description(self, description: str) -> None:
        """Update the free-text description."""
        self.__description = description

    # ------------------------------------------------------------------ #
    # Serialisation helpers
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Convert cup data to a dictionary for JSON storage."""
        return {
            "name": self.__name,
            "location": self.__location,
            "sport_type": self.__sport_type,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "description": self.__description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Cup":
        """Create a Cup object from a dictionary (e.g. loaded from JSON)."""
        return cls(
            name=data.get("name", "Hockey Cup"),
            location=data.get("location", ""),
            sport_type=data.get("sport_type", "Ice Hockey"),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            description=data.get("description", ""),
        )

    # ------------------------------------------------------------------ #
    # String representation
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        """Return a formatted multi-line summary of the cup."""
        return (
            f"  Name        : {self.__name}\n"
            f"  Location    : {self.__location}\n"
            f"  Sport type  : {self.__sport_type}\n"
            f"  Start date  : {self.__start_date}\n"
            f"  End date    : {self.__end_date}\n"
            f"  Description : {self.__description}"
        )
