# Task Tracker CLI

A lightweight, automated Command Line Interface (CLI) tool designed to track and manage tasks directly from the terminal. This project demonstrates systems-level programming practices, structured file system state manipulation using Python's native libraries, and strict input validation.

This tool is built specifically to practice core backend and DevOps automation patterns, focusing on robust data serialization and clean system execution.

## System Architecture & CLI Usage

The application accepts commands and arguments dynamically via terminal inputs.

```bash
# Adding a new task
python task_tracker.py add "Deploy production build"

# Updating a task description
python task_tracker.py update 1 "Optimize Docker configurations"

# Deleting a task
python task_tracker.py delete 1

# Progress Lifecycle Management
python task_tracker.py mark-in-progress 1
python task_tracker.py mark-done 1

# Global and Filtered Operational Queries
python task_tracker.py list
python task_tracker.py list done
python task_tracker.py list todo
python task_tracker.py list in-progress