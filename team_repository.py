# team_repository.py
from __future__ import annotations

# Defines TeamRepository, which manages all Team objects in memory.
# It is the single source of truth for teams during a program session.
# Responsibilities: add, remove, update, search, and retrieve teams.

from team import Team


class TeamRepository:
    """
    Manages Team objects in memory.

    Stores teams in a dictionary keyed by ID for O(1) look-up.
    Tracks the next available ID so IDs remain unique across sessions
    (the next_id is persisted to the data file by TeamStorage).

    Collaborations:
        - Team    : creates and holds Team instances.
        - UI      : calls repository methods for every user action.
        - TeamStorage : the repository's state is saved/loaded by storage.
    """

    def __init__(self):
        """Initialise an empty repository with next_id starting at 1."""
        self.__teams: dict[int, Team] = {}  # {team_id: Team}
        self.__next_id: int = 1

    # ------------------------------------------------------------------ #
    # ID management
    # ------------------------------------------------------------------ #

    def get_next_id(self) -> int:
        """Return the next ID that will be assigned to a new team."""
        return self.__next_id

    def set_next_id(self, next_id: int) -> None:
        """
        Set the next ID (called when loading persisted data so that
        IDs already used are never reused).
        """
        self.__next_id = next_id

    # ------------------------------------------------------------------ #
    # Create
    # ------------------------------------------------------------------ #

    def add_team(self, name: str, team_type: str, fee_paid: bool = False) -> Team:
        """
        Create a new Team, store it in the repository, and return it.
        The ID and creation date are assigned automatically.

        Args:
            name      : team name
            team_type : 'boys' or 'girls'
            fee_paid  : whether the fee has already been paid (default False)

        Returns:
            The newly created Team object.
        """
        team = Team(self.__next_id, name, team_type, fee_paid)
        self.__teams[self.__next_id] = team
        self.__next_id += 1
        return team

    def load_team(self, team: Team) -> None:
        """
        Insert an existing Team object into the repository without
        modifying the next_id. Used when loading data from file.

        Args:
            team : a Team object reconstructed from persistent storage
        """
        self.__teams[team.get_id()] = team

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #

    def get_team(self, team_id: int) -> Team | None:
        """
        Retrieve a single team by its ID.

        Returns:
            The Team if found, otherwise None.
        """
        return self.__teams.get(team_id)

    def get_all_teams(self) -> list[Team]:
        """Return all teams as a list (insertion order via dict)."""
        return list(self.__teams.values())

    def get_teams_by_type(self, team_type: str) -> list[Team]:
        """
        Return all teams matching the given type.

        Args:
            team_type : 'boys' or 'girls' (case-insensitive)
        """
        target = team_type.lower()
        return [t for t in self.__teams.values() if t.get_type() == target]

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update_team_name(self, team_id: int, name: str) -> bool:
        """
        Update the name of the team with the given ID.

        Returns:
            True if the team was found and updated, False otherwise.
        """
        team = self.get_team(team_id)
        if team:
            team.set_name(name)
            return True
        return False

    def update_team_type(self, team_id: int, team_type: str) -> bool:
        """
        Update the type ('boys'/'girls') of the team with the given ID.

        Returns:
            True if found and updated, False otherwise.
        """
        team = self.get_team(team_id)
        if team:
            team.set_type(team_type)
            return True
        return False

    def update_fee_paid(self, team_id: int, paid: bool) -> bool:
        """
        Update the fee-paid status of the team with the given ID.

        Returns:
            True if found and updated, False otherwise.
        """
        team = self.get_team(team_id)
        if team:
            team.set_fee_paid(paid)
            return True
        return False

    # ------------------------------------------------------------------ #
    # Cancellation
    # ------------------------------------------------------------------ #

    def cancel_team(self, team_id: int) -> bool:
        """
        Mark the team with the given ID as cancelled.

        Returns:
            True if found and cancelled, False otherwise.
        """
        team = self.get_team(team_id)
        if team:
            team.cancel()
            return True
        return False

    def reinstate_team(self, team_id: int) -> bool:
        """
        Reinstate a previously cancelled team.

        Returns:
            True if found and reinstated, False otherwise.
        """
        team = self.get_team(team_id)
        if team:
            team.reinstate()
            return True
        return False

    # ------------------------------------------------------------------ #
    # Delete
    # ------------------------------------------------------------------ #

    def remove_team(self, team_id: int) -> bool:
        """
        Permanently remove the team with the given ID.

        Returns:
            True if found and removed, False otherwise.
        """
        if team_id in self.__teams:
            del self.__teams[team_id]
            return True
        return False

    # ------------------------------------------------------------------ #
    # Search / filter
    # ------------------------------------------------------------------ #

    def search_by_name(self, query: str) -> list[Team]:
        """
        Return all teams whose name contains the query string
        (case-insensitive, partial match).

        Args:
            query : search string
        """
        q = query.lower()
        return [t for t in self.__teams.values() if q in t.get_name().lower()]

    def get_teams_by_payment_status(self, paid: bool) -> list[Team]:
        """
        Return active (non-cancelled) teams filtered by payment status.

        Args:
            paid : True to get teams that have paid, False for those that haven't
        """
        return [
            t for t in self.__teams.values()
            if t.is_fee_paid() == paid and not t.is_cancelled()
        ]

    # ------------------------------------------------------------------ #
    # Statistics
    # ------------------------------------------------------------------ #

    def get_statistics(self) -> dict:
        """
        Compute and return a statistics dictionary:
            total     : total number of teams (including cancelled)
            active    : teams that have NOT cancelled
            cancelled : teams that have cancelled
            paid      : active teams that have paid the fee
            paid_percent : percentage of active teams that have paid
        """
        all_teams = self.get_all_teams()
        total = len(all_teams)

        if total == 0:
            return {
                "total": 0,
                "active": 0,
                "cancelled": 0,
                "paid": 0,
                "paid_percent": 0.0,
            }

        cancelled = sum(1 for t in all_teams if t.is_cancelled())
        active = total - cancelled
        # Count only active teams that have paid (cancelled teams excluded)
        paid = sum(
            1 for t in all_teams if t.is_fee_paid() and not t.is_cancelled()
        )
        paid_percent = (paid / active * 100) if active > 0 else 0.0

        return {
            "total": total,
            "active": active,
            "cancelled": cancelled,
            "paid": paid,
            "paid_percent": paid_percent,
        }
