from browser import document, html

def set_cookie(name, value, days=7):
    """Sets a cookie with a specified name, value, and expiration time in days."""
    expires = f"; expires={days * 24 * 60 * 60}"
    document.cookie = f"{name}={value}{expires}; path=/"

def get_cookie(name):
    """Retrieves a cookie by name."""
    cookies = document.cookie.split("; ")
    for cookie in cookies:
        if cookie.startswith(f"{name}="):
            return cookie.split("=", 1)[1]
    return ""

def get_tasks() -> list[str]:
    """Fetches tasks from the 'tasks' cookie."""
    tasks = get_cookie("tasks")
    return tasks.strip(":").split(":") if tasks else []

def set_tasks(tasks: list[str]) -> None:
    """Saves tasks to the 'tasks' cookie."""
    tasks_str = ":".join(tasks)
    set_cookie("tasks", tasks_str)
    sync()

def add_task(event):
    """Adds a new task based on user input."""
    input_field = document["task-input"]
    tasks = get_tasks()
    tasks.append(input_field.value)
    set_tasks(tasks)
    input_field.value = ""

def remove_task(event):
    """Removes a task by clicking on it."""
    task = event.target.text
    tasks = get_tasks()
    if task in tasks:
        tasks.remove(task)
        set_tasks(tasks)

def sync():
    """Syncs the display with the tasks list."""
    tasks = get_tasks()
    items_div.clear()
    items_div.attach((html.DIV(i, id="todo-item") for i in tasks))
    for task in document.select("#todo-item"):
        task.bind("click", remove_task)

# Initialize
items_div = document["todo-items"]
set_tasks(get_tasks())  # Load tasks from cookie on start

# Set up event bindings
task_button = document["task-button"]
task_button.bind("click", add_task)
sync()

