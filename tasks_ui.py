import PySimpleGUI as sg
import fcntl

from typing import List

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TODAY = datetime.today().date()


def main() -> None:
    sg.theme("BluePurple")

    layout = [
        [sg.Text("To Do")],
        [
            sg.Listbox(values=_get_tasks(), size=(40, 10), key="tasks"),
            sg.Button("Done", key="done_btn"),
        ],
        [sg.Text("Done (Today)")],
        [
            sg.Listbox(
                values=_get_today_done_tasks(), size=(40, 10), key="completed_tasks"
            )
        ],
    ]

    window = sg.Window("ToDo App", layout)

    while True:
        event, values = window.Read()
        if event == "done_btn":
            _mark_as_done(values["tasks"][0])

            window.find_element("tasks").Update(values=_get_tasks())
            window.find_element("completed_tasks").Update(
                values=_get_today_done_tasks()
            )

        elif event is None:
            break


def _get_tasks() -> List[str]:
    tasks = set()
    with open("not_done_tasks.txt", "r") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        for line in file:
            tasks.add(line.strip())
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    return [task for task in tasks]


def _get_today_done_tasks() -> List[str]:
    tasks = []
    with open("done_tasks.txt", "r") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        for line in file:
            tasks.append(line.strip().split(";"))
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    return [task[1] for task in tasks if _is_date_today(task[0])]


def _mark_as_done(task) -> None:
    tasks = _get_tasks()
    tasks.remove(task)
    with open("not_done_tasks.txt", "w") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        for task in tasks:
            file.write(f"{task}\n")
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    with open("done_tasks.txt", "a") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        file.write(f"{datetime.now().strftime(DATE_FORMAT)};{task}\n")
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)


def _is_date_today(datestr: str) -> bool:
    return _to_datetime(datestr).date() == TODAY


def _to_datetime(datestr: str):
    return datetime.strptime(datestr, DATE_FORMAT)


if __name__ == "__main__":
    main()
