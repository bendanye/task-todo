import fcntl
import sys

if len(sys.argv) <= 1:
    print("Specify item to add")
    exit(1)

item = sys.argv[1]

with open("not_done_tasks.txt", "a") as file:
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)

    file.write(f"{item}\n")

    fcntl.flock(file.fileno(), fcntl.LOCK_UN)
