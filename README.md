# Hockey Cup Registration Manager

A Python command-line application for managing hockey cup team registrations, fee-payment status and event details. Developed as a programming coursework project during my MSc in Data Science at Dalarna University, Sweden.

The project demonstrates object-oriented design, separation of responsibilities and JSON persistence through a practical registration workflow.

## Features

- Register, view, update and delete teams.
- Search by team name and filter by team type or fee-payment status.
- Cancel a registration or reinstate a cancelled team.
- Record registration and cancellation dates.
- Mark participation fees as paid or unpaid.
- View registration totals, active and cancelled teams, and payment statistics.
- Edit cup information, including its name, location, dates and description.
- Save team records, cup details and the next team ID to a local JSON file.

The application manages registration and payment-status records. It does not process payments, schedule matches or calculate tournament results.

## Getting started

**Requirements:** Python 3.10 or later. No third-party packages are required.

Download or clone the repository, open a terminal in its root folder, and run:

```bash
python program.py
```

On systems where Python 3 is invoked separately:

```bash
python3 program.py
```

Run from the repository folder so the application uses the included `hockey_cup_data.json` file. The bundled cup details and team records provide example application state, rather than a current event listing.

## Example workflow

1. Choose **Add new team** to enter a team name, type and fee-payment status.
2. Choose **View team by ID** or **Search teams** to find a registration.
3. Use **Update team** to edit its details or change its payment status.
4. Use **Cancel / Reinstate team** to change registration status while retaining the record.
5. Open **Show statistics** to review participation and fee-payment figures.

Changes made through the menu trigger a save to the local JSON file. The application also attempts to save when exiting.

## Architecture

Five classes are organised across dedicated modules, with a separate entry point.

| File | Responsibility |
|---|---|
| `program.py` | Loads saved state, connects the components and starts the menu |
| `team.py` | `Team`: registration details, fee status, cancellation state and serialisation |
| `cup.py` | `Cup`: event metadata and serialisation |
| `team_repository.py` | `TeamRepository`: in-memory records, IDs, search, filtering and statistics |
| `team_storage.py` | `TeamStorage`: loading and saving JSON data |
| `ui.py` | `UI`: terminal menus, input handling and user interactions |
| `hockey_cup_data.json` | Saved cup metadata, team records and next-ID counter |

The repository separates team-management operations from file storage and terminal interaction. `Team` and `Cup` provide `to_dict()` and `from_dict()` helpers for transferring state to and from JSON.

## Persistence and scope

Data is stored in `hockey_cup_data.json` relative to the working directory. The file contains `next_id`, `cup` and `teams`. When no file exists, the application starts with an empty team list and default cup information.

The participation fee is defined as **1,500 SEK per team** in `Team.PARTICIPATION_FEE`. Fee status records whether payment has been marked as received; it is not connected to a payment provider.

This is a local, single-user coursework application using file-based storage. The implementation includes handling for common input and file errors, but does not provide database transactions, concurrent-user support or automatic backups.

## Skills demonstrated

- Python and object-oriented programming
- Encapsulation and modular application design
- Repository pattern and separation of concerns
- JSON serialisation and local persistence
- Command-line interfaces and input validation
- Type annotations and code documentation

## Academic context

Created as a Python programming project at Dalarna University as part of my Data Science master's studies.

Related coursework: [Python Programming MSc](https://github.com/iamalif/python-programming-msc).
