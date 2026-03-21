# team_storage.py
# Defines TeamStorage, which is responsible for persisting all program data
# (teams, next_id counter, and cup metadata) to a JSON file, and loading
# it back on startup. Auto-save is triggered after every change via the UI.

import json
import os

from team import Team
from cup import Cup


class TeamStorage:
    """
    Handles saving and loading all program data to/from a JSON file.

    The JSON file has the following top-level structure:
        {
          "next_id": <int>,
          "cup": { ...cup fields... },
          "teams": [ {...team dict...}, ... ]
        }

    Responsibilities:
        - save()  : write teams, next_id, and cup to the file
        - load()  : read and return teams, next_id, and cup data from the file

    Collaborations:
        - Team : serialised/deserialised via Team.to_dict() / Team.from_dict()
        - Cup  : serialised/deserialised via Cup.to_dict() / Cup.from_dict()
        - UI   : calls save() after every mutating operation (auto-save)
        - program.py : calls load() on startup to restore previous session
    """

    def __init__(self, filename: str = "hockey_cup_data.json"):
        """
        Initialise storage with a target filename.

        Args:
            filename : path to the JSON data file (default: hockey_cup_data.json)
        """
        self.__filename = filename

    # ------------------------------------------------------------------ #
    # Public interface
    # ------------------------------------------------------------------ #

    def get_filename(self) -> str:
        """Return the name of the data file being used."""
        return self.__filename

    def save(self, teams: list[Team], next_id: int, cup: Cup) -> bool:
        """
        Serialise all data and write it to the JSON file.

        Args:
            teams   : list of all Team objects currently in the repository
            next_id : the next available team ID (must be preserved)
            cup     : the Cup object with event metadata

        Returns:
            True on success, False if an I/O error occurs.
        """
        data = {
            "next_id": next_id,
            "cup": cup.to_dict(),
            "teams": [t.to_dict() for t in teams],
        }
        try:
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"\n[!] Error saving data to '{self.__filename}': {e}")
            return False

    def load(self) -> tuple[list[Team], int, dict]:
        """
        Read the JSON file and deserialise its contents.

        If the file does not exist, returns sensible defaults so the program
        starts cleanly on the first run.

        Returns:
            A tuple of:
                teams    : list of Team objects (may be empty)
                next_id  : the next available ID (at least 1)
                cup_data : raw dict of cup fields (empty dict if missing)
        """
        # No file yet – first run
        if not os.path.exists(self.__filename):
            return [], 1, {}

        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Reconstruct Team objects from their dicts
            teams = [Team.from_dict(t) for t in data.get("teams", [])]
            next_id = data.get("next_id", 1)

            # Ensure next_id is always greater than the highest existing ID
            # (guards against a corrupt or hand-edited file)
            if teams:
                max_id = max(t.get_id() for t in teams)
                if next_id <= max_id:
                    next_id = max_id + 1

            cup_data = data.get("cup", {})
            return teams, next_id, cup_data

        except json.JSONDecodeError as e:
            print(f"\n[!] Data file '{self.__filename}' is corrupted: {e}")
            print("    Starting with an empty data set.")
            return [], 1, {}
        except (KeyError, TypeError, ValueError) as e:
            print(f"\n[!] Unexpected data format in '{self.__filename}': {e}")
            print("    Starting with an empty data set.")
            return [], 1, {}
        except IOError as e:
            print(f"\n[!] Could not read '{self.__filename}': {e}")
            return [], 1, {}
