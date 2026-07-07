import json
import sys
from datetime import datetime
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


def update_task(task_id: int, new_description: str):
    """Finds a task by ID and updates its description and modification timestamp."""
    if not new_description.strip():
        print("Error: New description cannot be empty.")
        return
    tasks = load_tasks()

    # Search for the targeted task
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return

    print(f"Error: Task with ID {task_id} not found.")


def delete_task(task_id: int):
    """Removes a task from the dataset entirely based on its ID."""
    tasks = load_tasks()

    # Filter out the task with the matching ID
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        print(f"Error: Task with ID {task_id} not found.")
        return

    save_tasks(updated_tasks)
    print(f"Task {task_id} deleted successfully.")


def main():
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

    elif command == "update":
        if len(sys.argv) < 4:
            print(
                'Error: Missing arguments. Usage: python task_tracker.py update [id] "new description"'
            )
            return
        try:
            task_id = int(sys.argv[2])
            update_task(task_id, sys.argv[3])
        except ValueError:
            print("Error: Task ID must be an integer.")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Missing task ID. Usage: python task_tracker.py delete [id]")
            return
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be an integer.")
    else:
        print(f"Unknown command: '{command}'")


if __name__ == "__main__":
    main()
