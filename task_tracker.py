import json
from pathlib import Path

# Define the absolute target layout for our database storage file
STORAGE_FILE = Path("./tasks.json")


def initialize_storage():
    """Ensures the JSON databasee file exists in the execution directory.
    If it is missing, initialize it safely with an empty array wrapper."""

    if not STORAGE_FILE.exists():
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)


def load_tasks() -> list:
    """Reads and parses the tasks from the JSON database file."""
    initialize_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Emergency safety handling for corrupted files
        return []


def save_tasks(tasks: list):
    """Serializes and writes the complete task list state back onto disk."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)
