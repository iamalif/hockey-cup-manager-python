# ui.py
# Defines the UI class, which owns the entire command-line menu system.
# It translates user input into calls on the TeamRepository, and triggers
# TeamStorage auto-save after every mutating action.

from __future__ import annotations

import re
from datetime import datetime

from team import Team
from team_repository import TeamRepository
from team_storage import TeamStorage
from cup import Cup


class UI:
    """
    Command-line interface for the Hockey Cup Management System.

    Provides a main menu and sub-menus for every operation.
    All user-facing output and input validation lives here so that the
    other classes (Team, TeamRepository, Cup, TeamStorage) remain free
    of presentation concerns.

    Collaborations:
        - TeamRepository : called for all data operations (CRUD, search, stats)
        - TeamStorage    : called for auto-save after every mutation
        - Cup            : displayed and edited through the cup-info menu
        - Team           : PARTICIPATION_FEE class variable displayed to users
    """

    # Width of the separator lines used in menus
    _LINE_WIDTH = 52

    def __init__(
        self,
        repository: TeamRepository,
        storage: TeamStorage,
        cup: Cup,
    ):
        """
        Initialise the UI with the shared repository, storage, and cup objects.

        Args:
            repository : the in-memory store for all teams
            storage    : handles file persistence
            cup        : the cup event metadata object
        """
        self.__repository = repository
        self.__storage = storage
        self.__cup = cup

    # ================================================================== #
    # Public entry point
    # ================================================================== #

    def run(self) -> None:
        """Start the main menu loop. Runs until the user chooses to exit."""
        self.__print_header()

        while True:
            self.__display_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.__add_team()
            elif choice == "2":
                self.__view_team()
            elif choice == "3":
                self.__list_teams_menu()
            elif choice == "4":
                self.__update_team()
            elif choice == "5":
                self.__delete_team()
            elif choice == "6":
                self.__cancel_reinstate_menu()
            elif choice == "7":
                self.__search_teams_menu()
            elif choice == "8":
                self.__show_statistics()
            elif choice == "9":
                self.__cup_info_menu()
            elif choice == "0":
                self.__exit_program()
                break
            else:
                self.__error("Invalid choice. Please enter a number from the menu.")

    # ================================================================== #
    # Main menu display
    # ================================================================== #

    def __print_header(self) -> None:
        """Print a welcome header with basic cup information."""
        print("\n" + "=" * self._LINE_WIDTH)
        print("      HOCKEY CUP MANAGEMENT SYSTEM")
        print("=" * self._LINE_WIDTH)
        print(f"  Cup      : {self.__cup.get_name()}")
        print(f"  Location : {self.__cup.get_location()}")
        dates = f"{self.__cup.get_start_date()} to {self.__cup.get_end_date()}"
        print(f"  Dates    : {dates}")
        print("=" * self._LINE_WIDTH)

    def __display_main_menu(self) -> None:
        """Print the main menu options."""
        print("\n--- MAIN MENU " + "-" * 38)
        print("  1. Add new team")
        print("  2. View team by ID")
        print("  3. List teams")
        print("  4. Update team")
        print("  5. Delete team")
        print("  6. Cancel / Reinstate team")
        print("  7. Search teams")
        print("  8. Show statistics")
        print("  9. Cup information")
        print("  0. Exit")
        print("-" * self._LINE_WIDTH)

    # ================================================================== #
    # 1 – Add new team
    # ================================================================== #

    def __add_team(self) -> None:
        """Prompt the user for details and register a new team."""
        print("\n--- ADD NEW TEAM " + "-" * 35)

        # Team name (required, non-empty)
        name = self.__prompt_non_empty("Team name")
        if name is None:
            return

        # Team type: boys or girls (validated, with retry; None means cancelled)
        team_type = self.__prompt_team_type()
        if team_type is None:
            return

        # Fee-paid status (y/n, with retry)
        fee_paid = self.__prompt_yes_no(
            f"Has the registration fee ({Team.PARTICIPATION_FEE} SEK) been paid?"
        )

        # Create team and auto-save
        team = self.__repository.add_team(name, team_type, fee_paid)
        self.__auto_save()

        print(f"\n  [+] Team registered successfully!")
        print(f"  {team}")

    # ================================================================== #
    # 2 – View team by ID
    # ================================================================== #

    def __view_team(self) -> None:
        """Display all details for a single team."""
        print("\n--- VIEW TEAM BY ID " + "-" * 32)

        team_id = self.__prompt_team_id()
        if team_id is None:
            return

        team = self.__repository.get_team(team_id)
        if team is None:
            self.__error(f"No team found with ID {team_id}.")
            return

        print()
        self.__print_team_detail(team)

    # ================================================================== #
    # 3 – List teams (sub-menu)
    # ================================================================== #

    def __list_teams_menu(self) -> None:
        """Sub-menu: list all teams, boys only, or girls only."""
        print("\n--- LIST TEAMS " + "-" * 37)
        print("  1. All teams")
        print("  2. Boys teams only")
        print("  3. Girls teams only")
        print("  0. Back")

        choice = input("  Your choice: ").strip()

        if choice == "1":
            self.__display_team_list(
                self.__repository.get_all_teams(), "ALL TEAMS"
            )
        elif choice == "2":
            self.__display_team_list(
                self.__repository.get_teams_by_type("boys"), "BOYS TEAMS"
            )
        elif choice == "3":
            self.__display_team_list(
                self.__repository.get_teams_by_type("girls"), "GIRLS TEAMS"
            )
        elif choice == "0":
            return
        else:
            self.__error("Invalid choice.")

    def __display_team_list(self, teams: list[Team], title: str) -> None:
        """Print a formatted table of teams."""
        print(f"\n--- {title} " + "-" * (self._LINE_WIDTH - len(title) - 5))

        if not teams:
            print("  (no teams found)")
            return

        # Table header
        print(
            f"  {'ID':>4}  {'Name':<25}  {'Type':<6}  {'Fee':<9}  Status"
        )
        print("  " + "-" * 56)

        for t in teams:
            fee = "Paid" if t.is_fee_paid() else "Not Paid"
            status = "CANCELLED" if t.is_cancelled() else "Active"
            print(
                f"  {t.get_id():>4}  {t.get_name():<25}  "
                f"{t.get_type().capitalize():<6}  {fee:<9}  {status}"
            )

        print(f"\n  Total: {len(teams)} team(s)")

    # ================================================================== #
    # 4 – Update team
    # ================================================================== #

    def __update_team(self) -> None:
        """Allow the user to edit a team's name, type, or fee-paid status."""
        print("\n--- UPDATE TEAM " + "-" * 36)

        team_id = self.__prompt_team_id()
        if team_id is None:
            return

        team = self.__repository.get_team(team_id)
        if team is None:
            self.__error(f"No team found with ID {team_id}.")
            return

        if team.is_cancelled():
            self.__error(
                f"Team '{team.get_name()}' is cancelled. "
                "Reinstate it first before updating."
            )
            return

        print(f"\n  Current: {team}")
        print("\n  What would you like to update?")
        print("    1. Name")
        print("    2. Type (boys / girls)")
        print("    3. Toggle fee-paid status")
        print("    0. Back")

        choice = input("  Your choice: ").strip()

        if choice == "1":
            # Update name
            name = self.__prompt_non_empty("New team name")
            if name is None:
                return
            self.__repository.update_team_name(team_id, name)
            self.__auto_save()
            print(f"\n  [+] Name updated to '{name}'.")

        elif choice == "2":
            # Update type
            print(f"  Current type: {team.get_type()}")
            team_type = self.__prompt_team_type()
            if team_type is None:
                return
            self.__repository.update_team_type(team_id, team_type)
            self.__auto_save()
            print(f"\n  [+] Type updated to '{team_type}'.")

        elif choice == "3":
            # Toggle fee-paid status
            new_status = not team.is_fee_paid()
            self.__repository.update_fee_paid(team_id, new_status)
            self.__auto_save()
            label = "Paid" if new_status else "Not Paid"
            print(f"\n  [+] Fee status toggled to: {label}.")

        elif choice == "0":
            return

        else:
            self.__error("Invalid choice.")

    # ================================================================== #
    # 5 – Delete team
    # ================================================================== #

    def __delete_team(self) -> None:
        """Permanently remove a team after user confirmation."""
        print("\n--- DELETE TEAM " + "-" * 36)

        team_id = self.__prompt_team_id()
        if team_id is None:
            return

        team = self.__repository.get_team(team_id)
        if team is None:
            self.__error(f"No team found with ID {team_id}.")
            return

        print(f"\n  Team to delete: {team}")
        confirm = self.__prompt_yes_no(
            "Are you sure you want to permanently delete this team?"
        )

        if confirm:
            self.__repository.remove_team(team_id)
            self.__auto_save()
            print(f"\n  [+] Team (ID: {team_id}) deleted.")
        else:
            print("\n  [-] Deletion cancelled.")

    # ================================================================== #
    # 6 – Cancel / Reinstate team
    # ================================================================== #

    def __cancel_reinstate_menu(self) -> None:
        """Cancel an active team or reinstate a cancelled one."""
        print("\n--- CANCEL / REINSTATE TEAM " + "-" * 24)

        team_id = self.__prompt_team_id()
        if team_id is None:
            return

        team = self.__repository.get_team(team_id)
        if team is None:
            self.__error(f"No team found with ID {team_id}.")
            return

        print(f"\n  Team: {team}")

        if team.is_cancelled():
            # Offer to reinstate
            confirm = self.__prompt_yes_no(
                "This team is already cancelled. Reinstate it?"
            )
            if confirm:
                self.__repository.reinstate_team(team_id)
                self.__auto_save()
                print(f"\n  [+] Team '{team.get_name()}' reinstated.")
            else:
                print("\n  [-] No changes made.")
        else:
            # Offer to cancel
            confirm = self.__prompt_yes_no(
                f"Cancel team '{team.get_name()}'?"
            )
            if confirm:
                self.__repository.cancel_team(team_id)
                self.__auto_save()
                print(
                    f"\n  [+] Team '{team.get_name()}' cancelled "
                    f"on {team.get_cancellation_date()}."
                )
            else:
                print("\n  [-] Cancellation aborted.")

    # ================================================================== #
    # 7 – Search teams (sub-menu)
    # ================================================================== #

    def __search_teams_menu(self) -> None:
        """Sub-menu: search by name, or filter by payment status."""
        print("\n--- SEARCH TEAMS " + "-" * 35)
        print("  1. Search by name")
        print("  2. Filter by payment status")
        print("  0. Back")

        choice = input("  Your choice: ").strip()

        if choice == "1":
            # Search by name (partial, case-insensitive)
            query = self.__prompt_non_empty("Name to search for")
            if query is None:
                return
            results = self.__repository.search_by_name(query)
            self.__display_team_list(results, f"RESULTS FOR '{query.upper()}'")

        elif choice == "2":
            # Filter by payment status
            print("  1. Teams that have paid")
            print("  2. Teams that have NOT paid")
            sub = input("  Your choice: ").strip()

            if sub == "1":
                results = self.__repository.get_teams_by_payment_status(True)
                self.__display_team_list(results, "TEAMS WITH FEE PAID")
            elif sub == "2":
                results = self.__repository.get_teams_by_payment_status(False)
                self.__display_team_list(results, "TEAMS WITH FEE NOT PAID")
            else:
                self.__error("Invalid choice.")

        elif choice == "0":
            return

        else:
            self.__error("Invalid choice.")

    # ================================================================== #
    # 8 – Statistics
    # ================================================================== #

    def __show_statistics(self) -> None:
        """Display aggregate statistics about all registered teams."""
        print("\n--- STATISTICS " + "-" * 37)

        stats = self.__repository.get_statistics()

        print(f"  Total teams registered : {stats['total']}")
        print(f"  Active teams           : {stats['active']}")
        print(f"  Cancelled teams        : {stats['cancelled']}")
        print(f"  Active teams paid fee  : {stats['paid']}")
        print(f"  Fee payment rate       : {stats['paid_percent']:.1f}%"
              " (of active teams)")
        print(f"  Participation fee      : {Team.PARTICIPATION_FEE} SEK per team")

    # ================================================================== #
    # 9 – Cup information
    # ================================================================== #

    def __cup_info_menu(self) -> None:
        """Display current cup information with an option to edit it."""
        print("\n--- CUP INFORMATION " + "-" * 32)
        print(self.__cup)
        print()
        print("  1. Edit cup information")
        print("  0. Back")

        choice = input("  Your choice: ").strip()

        if choice == "1":
            self.__edit_cup()
        elif choice == "0":
            return
        else:
            self.__error("Invalid choice.")

    def __edit_cup(self) -> None:
        """Prompt the user to update any cup field (press Enter to keep current)."""
        print("\n  Edit cup information (press Enter to keep current value)")

        # Helper: update a string field if the user provides a non-empty value
        def update_string(label: str, getter, setter) -> None:
            val = input(f"  {label} [{getter()}]: ").strip()
            if val:
                setter(val)

        update_string("Cup name", self.__cup.get_name, self.__cup.set_name)
        update_string("Location", self.__cup.get_location, self.__cup.set_location)
        update_string("Sport type", self.__cup.get_sport_type, self.__cup.set_sport_type)

        # Date fields require format validation
        self.__update_cup_date(
            "Start date (YYYY-MM-DD)",
            self.__cup.get_start_date,
            self.__cup.set_start_date,
        )
        self.__update_cup_date(
            "End date   (YYYY-MM-DD)",
            self.__cup.get_end_date,
            self.__cup.set_end_date,
        )

        update_string("Description", self.__cup.get_description, self.__cup.set_description)

        self.__auto_save()
        print("\n  [+] Cup information updated.")

    def __update_cup_date(self, label: str, getter, setter) -> None:
        """
        Prompt for a date field. Validates YYYY-MM-DD format.
        Keeps the current value if the user presses Enter.
        """
        while True:
            val = input(f"  {label} [{getter()}]: ").strip()
            if not val:
                return  # keep current
            if self.__is_valid_date(val):
                setter(val)
                return
            self.__error("Invalid date format. Please use YYYY-MM-DD.")

    # ================================================================== #
    # 0 – Exit
    # ================================================================== #

    def __exit_program(self) -> None:
        """Save all data and exit cleanly."""
        print("\n  Saving data...", end="")
        if self.__auto_save():
            print(" done.")
        print("\n  Goodbye! See you at the cup!\n")

    # ================================================================== #
    # Auto-save
    # ================================================================== #

    def __auto_save(self) -> bool:
        """
        Persist the current state of all teams and cup data to file.
        Called automatically after every mutating operation.

        Returns:
            True if save succeeded, False otherwise.
        """
        teams = self.__repository.get_all_teams()
        next_id = self.__repository.get_next_id()
        return self.__storage.save(teams, next_id, self.__cup)

    # ================================================================== #
    # Team detail formatter
    # ================================================================== #

    def __print_team_detail(self, team: Team) -> None:
        """Print a full detail block for a single team."""
        status = "CANCELLED" if team.is_cancelled() else "Active"
        fee = "Yes" if team.is_fee_paid() else "No"

        print(f"  {'ID':<18}: {team.get_id()}")
        print(f"  {'Name':<18}: {team.get_name()}")
        print(f"  {'Type':<18}: {team.get_type().capitalize()}")
        print(f"  {'Registered on':<18}: {team.get_date_created()}")
        print(f"  {'Fee paid':<18}: {fee}")
        print(f"  {'Status':<18}: {status}")

        if team.is_cancelled():
            print(f"  {'Cancelled on':<18}: {team.get_cancellation_date()}")

        print(f"  {'Participation fee':<18}: {Team.PARTICIPATION_FEE} SEK")

    # ================================================================== #
    # Input helpers
    # ================================================================== #

    def __prompt_non_empty(self, label: str) -> str | None:
        """
        Prompt for a required text field.
        Returns the trimmed value, or None if the user enters nothing
        (which returns the caller to the main menu).
        """
        value = input(f"  {label} (or press Enter to cancel): ").strip()
        if not value:
            print("\n  [-] Input cancelled. Returning to main menu.")
            return None
        return value

    def __prompt_team_id(self) -> int | None:
        """
        Prompt for a team ID and validate it as a positive integer.
        Returns the integer ID, or None on invalid/empty input.
        """
        raw = input("  Enter team ID (or press Enter to cancel): ").strip()
        if not raw:
            print("\n  [-] Cancelled. Returning to main menu.")
            return None
        try:
            team_id = int(raw)
            if team_id <= 0:
                self.__error("ID must be a positive integer.")
                return None
            return team_id
        except ValueError:
            self.__error(f"'{raw}' is not a valid ID. Please enter a whole number.")
            return None

    def __prompt_team_type(self) -> str | None:
        """
        Prompt for a team type until the user enters 'boys' or 'girls'.
        Returns None if the user presses Enter without typing (cancels the operation).
        """
        while True:
            value = input("  Team type (boys / girls, or press Enter to cancel): ").strip().lower()
            if not value:
                print("\n  [-] Input cancelled. Returning to main menu.")
                return None
            if value in ("boys", "girls"):
                return value
            self.__error("Please enter 'boys' or 'girls'.")

    def __prompt_yes_no(self, question: str) -> bool:
        """
        Ask a yes/no question and loop until a valid answer is given.

        Args:
            question : the question text (without the (y/n) suffix)

        Returns:
            True for yes, False for no.
        """
        while True:
            answer = input(f"  {question} (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            self.__error("Please enter 'y' (yes) or 'n' (no).")

    # ================================================================== #
    # Validation helpers
    # ================================================================== #

    @staticmethod
    def __is_valid_date(value: str) -> bool:
        """Return True if value is a real calendar date in strict YYYY-MM-DD format.
        The regex enforces exactly 4-2-2 digits; strptime then confirms the date exists."""
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ================================================================== #
    # Output helpers
    # ================================================================== #

    @staticmethod
    def __error(message: str) -> None:
        """Print a standardised error message."""
        print(f"\n  [!] {message}")
