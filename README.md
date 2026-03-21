# hockey-cup-manager-python

A Python command-line application to manage team registrations for a
hockey cup event, built using a professional multi-class OOP architecture.

## About
This program allows organisers to manage all aspects of a hockey cup —
registering teams, tracking fee payments, handling cancellations and
reinstatements, and viewing event statistics. All data is persisted
across sessions using a single JSON file. Built as a personal OOP and
JSON practice project.

## Features
- Four classes across dedicated modules: Team, Cup, TeamRepository,
  TeamStorage
- Auto-incrementing unique team IDs preserved across sessions
- Full CRUD operations on teams
- Cancel and reinstate teams with automatic cancellation date recording
- Mark teams as fee paid or unpaid
- Filter teams by type (boys/girls) or payment status
- Search teams by name (partial, case-insensitive)
- View and edit cup event metadata (name, location, dates, description)
- Team statistics: total, active, cancelled, paid, paid percentage
- Repository pattern for clean separation of data and logic
- Serialisation helpers (to_dict / from_dict) on Team and Cup classes
- Auto-save after every operation — no manual saving required
- Robust error handling for corrupted or missing JSON files
- Type hints throughout for code clarity
- Thoroughly commented and docstringed throughout for readability

## Project Structure
```
hockey-cup-manager-python/
│
├── program.py           ← entry point, wires all components together
├── team.py              ← Team class with serialisation helpers
├── cup.py               ← Cup class with event metadata
├── team_repository.py   ← in-memory data store and business logic
├── team_storage.py      ← JSON persistence layer
├── ui.py                ← user interface and menu loop
└── hockey_cup_data.json ← persisted data (auto-generated)
```

## How to Run
```bash
python program.py
```

## Built With
- Python 3
- Multi-class OOP — Team, Cup, TeamRepository, TeamStorage, UI
- Repository pattern for clean separation of concerns
- JSON module for nested data persistence
- Type hints for improved code readability
- Serialisation helpers (to_dict / from_dict class methods)
- Robust error handling for file I/O and data integrity

## Data Persistence
All team and cup data is automatically saved to hockey_cup_data.json
after every operation. The file preserves team IDs, creation dates,
cancellation history, and cup metadata across sessions. Corrupted or
missing files are handled gracefully without crashing the program.

## Architecture
This project follows a layered architecture:

| Layer | File | Responsibility |
|-------|------|----------------|
| Data model | team.py, cup.py | Define entities and serialisation |
| Repository | team_repository.py | Manage teams in memory |
| Storage | team_storage.py | Handle JSON persistence |
| UI | ui.py | User interaction and menu |
| Entry point | program.py | Wire components and launch |
