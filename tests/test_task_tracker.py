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


if __name__ == "__main__":
    unittest.main()
