# team.py
# Defines the Team class, which represents a single hockey team
# participating in the cup. Each team is stored as an object with
# private attributes accessed through getters and setters.

from datetime import date


class Team:
    """
    Represents a hockey team registered for the cup.

    Attributes (private):
        __id              : unique integer identifier (auto-assigned)
        __date_created    : date the team was registered (YYYY-MM-DD)
        __name            : team name
        __type            : team gender category - 'boys' or 'girls'
        __fee_paid        : whether the participation fee has been paid
        __cancelled       : whether the team has cancelled its participation
        __cancellation_date: date of cancellation in YYYY-MM-DD format, or None

    Class variable:
        PARTICIPATION_FEE : the standard fee every team must pay (SEK).
                            Stored as a class variable because it applies
                            equally to all Team instances.
    """

    # Class variable: the fee every team must pay to participate.
    # Defined here so it belongs to the class, not to any single instance.
    PARTICIPATION_FEE = 1500  # SEK

    def __init__(
        self,
        team_id: int,
        name: str,
        team_type: str,
        fee_paid: bool = False,
        date_created: str = None,
        cancelled: bool = False,
        cancellation_date: str = None,
    ):
        """
        Initialise a Team object.

        Args:
            team_id         : unique integer ID (assigned by TeamRepository)
            name            : name of the team
            team_type       : 'boys' or 'girls'
            fee_paid        : True if the participation fee has been paid
            date_created    : creation date string (YYYY-MM-DD); defaults to today
            cancelled       : True if the team has cancelled
            cancellation_date: date of cancellation (YYYY-MM-DD), or None
        """
        self.__id = team_id
        # Use today's date if no creation date is provided (new team)
        self.__date_created = (
            date_created if date_created else date.today().strftime("%Y-%m-%d")
        )
        self.__name = name
        self.__type = team_type.lower()  # normalise to lowercase
        self.__fee_paid = fee_paid
        self.__cancelled = cancelled
        self.__cancellation_date = cancellation_date

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    def get_id(self) -> int:
        """Return the unique team ID."""
        return self.__id

    def get_date_created(self) -> str:
        """Return the date the team was created (YYYY-MM-DD)."""
        return self.__date_created

    def get_name(self) -> str:
        """Return the team name."""
        return self.__name

    def get_type(self) -> str:
        """Return the team type ('boys' or 'girls')."""
        return self.__type

    def is_fee_paid(self) -> bool:
        """Return True if the participation fee has been paid."""
        return self.__fee_paid

    def is_cancelled(self) -> bool:
        """Return True if the team has cancelled its participation."""
        return self.__cancelled

    def get_cancellation_date(self) -> str:
        """Return the cancellation date (YYYY-MM-DD), or None."""
        return self.__cancellation_date

    # ------------------------------------------------------------------ #
    # Setters
    # ------------------------------------------------------------------ #

    def set_name(self, name: str) -> None:
        """Update the team name."""
        self.__name = name

    def set_type(self, team_type: str) -> None:
        """Update the team type. Must be 'boys' or 'girls'."""
        self.__type = team_type.lower()

    def set_fee_paid(self, paid: bool) -> None:
        """Update the fee-paid status."""
        self.__fee_paid = paid

    # ------------------------------------------------------------------ #
    # Cancellation handling
    # ------------------------------------------------------------------ #

    def cancel(self) -> None:
        """Mark the team as cancelled, recording today as the cancellation date."""
        self.__cancelled = True
        self.__cancellation_date = date.today().strftime("%Y-%m-%d")

    def reinstate(self) -> None:
        """Reinstate a cancelled team, clearing the cancellation date."""
        self.__cancelled = False
        self.__cancellation_date = None

    # ------------------------------------------------------------------ #
    # Serialisation helpers (used by TeamStorage for JSON persistence)
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Convert the team to a dictionary for JSON serialisation."""
        return {
            "id": self.__id,
            "date_created": self.__date_created,
            "name": self.__name,
            "type": self.__type,
            "fee_paid": self.__fee_paid,
            "cancelled": self.__cancelled,
            "cancellation_date": self.__cancellation_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """
        Create a Team object from a dictionary (e.g. loaded from JSON).
        This preserves the original ID and creation date.
        """
        return cls(
            team_id=data["id"],
            name=data["name"],
            team_type=data["type"],
            fee_paid=data.get("fee_paid", False),
            date_created=data.get("date_created"),
            cancelled=data.get("cancelled", False),
            cancellation_date=data.get("cancellation_date"),
        )

    # ------------------------------------------------------------------ #
    # String representation
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        """Return a concise one-line string representation of the team."""
        fee_status = "Paid" if self.__fee_paid else "Not Paid"
        status = " [CANCELLED]" if self.__cancelled else ""
        return (
            f"ID: {self.__id:>4} | {self.__name:<25} | "
            f"{self.__type.capitalize():<6} | {fee_status:<8} | "
            f"Created: {self.__date_created}{status}"
        )
