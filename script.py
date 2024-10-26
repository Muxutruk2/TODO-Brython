from browser import document, html
from browser.local_storage import storage

storage["tasks"] = ""

def get_tasks() -> list[str]:
    return storage['tasks'].strip(":").split(":")

def set_tasks(tasks: list[str]) -> None:
    storage['tasks'] = ""
    storage['tasks'] = ":".join(tasks)
    sync()

def add_task(event):
    input_field = document["task-input"]
    storage['tasks'] += f":{input_field.value}"
    sync()

def remove_task(event):
    task = event.target.text
    tasks = get_tasks()
    tasks.remove(task)
    set_tasks(tasks)

def sync():
    tasks = get_tasks()
    items_div.clear()
    items_div.attach((html.DIV(i, id="todo-item") for i in tasks))
    for task in document.select("#todo-item"):
        task.bind("click", remove_task)

items_div = document["todo-items"]

set_tasks([str(i) for i in range(10)])

task_button = document["task-button"]

task_button.bind("click", add_task)
sync()

