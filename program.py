# program.py
# Entry point for the Hockey Cup Management System.
# This is the only file that instantiates all top-level objects and
# wires them together before starting the UI.

from team_repository import TeamRepository
from team_storage import TeamStorage
from cup import Cup
from ui import UI


def main() -> None:
    """
    Initialise all components, load persisted data, and launch the UI.

    Startup sequence:
        1. Create a TeamStorage instance (points to the JSON data file).
        2. Load any previously saved data (teams, next_id, cup metadata).
        3. Restore the Cup object from saved data, or create a default one
           if this is the first time the program is run.
        4. Restore TeamRepository state (teams + next_id counter).
        5. Hand control to the UI, which runs the main menu loop.
    """
    # --- Storage ---
    storage = TeamStorage("hockey_cup_data.json")

    # --- Load persisted data ---
    teams, next_id, cup_data = storage.load()

    # --- Cup ---
    # Use saved cup data if available; otherwise create sensible defaults.
    if cup_data:
        cup = Cup.from_dict(cup_data)
    else:
        cup = Cup(
            name="Youth Hockey Cup 2025",
            location="Stockholm",
            sport_type="Ice Hockey",
            start_date="2025-06-14",
            end_date="2025-06-16",
            description="Annual youth hockey tournament.",
        )

    # --- Repository ---
    repository = TeamRepository()
    repository.set_next_id(next_id)   # preserve IDs across restarts
    for team in teams:
        repository.load_team(team)    # re-insert each saved team

    # --- UI ---
    ui = UI(repository, storage, cup)
    ui.run()


# Only run main() when this file is executed directly, not when imported.
if __name__ == "__main__":
    main()
