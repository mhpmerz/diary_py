# Diary PY

A modern diary application built with Python and CustomTkinter for creating and managing daily notes in a calendar interface.

## Features

- **Two-Panel Layout**: Calendar overview on the left, entry editor on the right
- **Month Tabs**: Easy navigation between months with tabbed interface
- **Year Selection**: Configurable year range (currently 1998-2025)
- **Day Indicators**: Clickable day buttons with visual indicators for entries with content
- **Visual Feedback**: Green buttons indicate days with saved content, gray for empty days
- **German Date Format**: Displays dates in German format (e.g., "Samstag, 18.10.2025")
- **Database Storage**: SQLite database for persistent storage of diary entries
- **Real-time Updates**: Button colors update immediately when content is saved

## Requirements

- Python 3.14+
- CustomTkinter
- SQLite3 (included with Python)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd diary_py
```

2. Install dependencies:
```bash
pip install customtkinter
```

## Usage

Run the application using one of these methods:

**Method 1 - Using the launcher script (recommended):**
```bash
python run_diary.py
```

**Method 2 - Direct module execution:**
```bash
python -m src.main.main
```

### How to Use

1. **Select a Year**: Use the dropdown in the top-left to select a year
2. **Choose a Month**: Click on the month tabs to navigate between months
3. **Select a Day**: Click on any day button to open the entry editor
4. **Write Your Entry**: Type your diary entry in the text area on the right
5. **Save**: Click the "Save Entry" button to persist your entry to the database

### Visual Indicators

- **Gray Buttons**: Days without any content
- **Green Buttons**: Days with saved diary entries

## Database Schema

The application uses a simple SQLite database with one table:

```sql
CREATE TABLE diary_entries (
    date TEXT PRIMARY KEY,  -- Format: YYYY-MM-DD
    content TEXT            -- Diary entry content
)
```

## Building Executable

To create a standalone executable:

```bash
python -m PyInstaller src/main/main.py --onefile --noconsole
```

The executable will be created in the `dist/` directory.

## Project Structure

```
diary_py/
├── src/main/
│   ├── main.py              # Main application
│   └── database/
│       └── checker.py       # Database utilities
├── datenbank.db            # SQLite database file
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## License

GNU General Public License v3.0