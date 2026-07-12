import json
import sys
import unittest
from pathlib import Path

# Allowing our test folder to find the task_tracker module in the parent folder
sys.path.append(str(Path(__file__).resolve().parent.parent))
import task_tracker

# Force the application to use a separate, temporary test database file
TEST_STORAGE = Path("./test_tasks.json")
task_tracker.STORAGE_FILE = TEST_STORAGE


class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        """Runs before every single test to ensure a clean state."""
        if TEST_STORAGE.exists():
            TEST_STORAGE.unlink()

    def tearDown(self):
        """Cleans up and removes the test file after every test finishes."""
        if TEST_STORAGE.exists():
            TEST_STORAGE.unlink()

    def test_add_task_creates_file_and_task(self):
        """Verify that adding a task correctly instantiates the database and structure."""
        # Execute the add_task logic directly
        task_tracker.add_task("Test automation script")

        # Assertions: Verify file creation and content consistency
        self.assertTrue(TEST_STORAGE.exists())

        with open(TEST_STORAGE, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["description"], "Test automation script")
        self.assertEqual(data[0]["status"], "todo")
        self.assertEqual(data[0]["id"], 1)

    def test_update_task_modifies_description(self):
        """Verify that a task's description can be updated dynamically."""
        task_tracker.add_task("Original description")

        # Update task ID 1
        task_tracker.update_task(1, "Updated description")

        tasks = task_tracker.load_tasks()
        self.assertEqual(tasks[0]["description"], "Updated description")
        # Ensure the updatedAt timestamp changed or existence
        self.assertIn("updatedAt", tasks[0])

    def test_delete_task_removes_from_storage(self):
        """Verify that a task is cleanly removed from the JSON database."""
        task_tracker.add_task("Task to delete")
        self.assertEqual(len(task_tracker.load_tasks()), 1)
        # Delete task ID 1
        task_tracker.delete_task(1)
        tasks = task_tracker.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_update_task_status(self):
        """Verify lifecycle progress transitions change states properly."""
        task_tracker.add_task("Lifecycle target")

        # Transition state to active progress
        task_tracker.update_task_status(1, "in-progress")
        tasks = task_tracker.load_tasks()
        self.assertEqual(tasks[0]["status"], "in-progress")

        # Transition state to completed
        task_tracker.update_task_status(1, "done")
        tasks = task_tracker.load_tasks()
        self.assertEqual(tasks[0]["status"], "done")

    def test_add_empty_description_fails(self):
        """Verify that empty description are rejected."""
        task_tracker.add_task("")
        tasks = task_tracker.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_nonexistent_task(self):
        """Verify deleting a non-existent task doesn't crash."""
        task_tracker.add_task("Real task")
        task_tracker.delete_task(999)
        tasks = task_tracker.load_tasks()
        self.assertEqual(len(tasks), 1)

    def test_list_tasks_by_status(self):
        """Verify status filtering works correctly."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.update_task_status(1, "done")

        tasks = task_tracker.load_tasks()
        done_tasks = [t for t in tasks if t["status"] == "done"]
        todo_tasks = [t for t in tasks if t["status"] == "todo"]

        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(len(todo_tasks), 1)


if __name__ == "__main__":
    unittest.main()
