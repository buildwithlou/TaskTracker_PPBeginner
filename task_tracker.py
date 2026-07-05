import datetime
import json
import sys
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


def add_task(description: str):
    """Creates a new task and appends it to the storage pipeline."""
    if not description.strip():
        print("Error: Task description cannot be empty.")
        return

    tasks = load_tasks()

    # Auto-increment dynamic ID strategy
    next_id = max([task["id"] for task in tasks], default=0) + 1

    current_time = datetime.now().isoformat()

    new_task = {
        "id": next_id,
        "description": description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added succesfully (ID: {next_id})")


def main():
    # sys.arg[0] is the script name. We check for arguments following it.
    if len(sys.argv) < 2:
        print("Usage: python task_tracker.py [command] [arguments]")
        print("Commands: add, upadte, delete, mark-in-progress, mark-done, list")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print(
                'Error: Missing description. Usage: python task_tracker.py add "description"'
            )
            return
        add_task(sys.argv[2])

    else:
        print(f"Unknown command: '{command}'")


if __name__ == "__main__":
    main()
