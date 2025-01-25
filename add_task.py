import fcntl
import sys
import os

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

if len(sys.argv) <= 1:
    print("Specify item to add")
    exit(1)

item = sys.argv[1]

with open(f"{SCRIPT_DIR}/not_done_tasks.txt", "a") as file:
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)

    file.write(f"{item}\n")

    fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    print(f"Added new task: {item}")
