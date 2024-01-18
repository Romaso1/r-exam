import json

# Клас Проект
class Project:
    def __init__(self, name, deadline, manager, tasks=[]):
        self.name = name
        self.deadline = deadline
        self.manager = manager
        self.tasks = tasks

    def add_task(self, task):
        self.tasks.append(task)

    def update_task(self, task_id, new_task):
        self.tasks[task_id] = new_task

    def get_status(self):
        status = "Завершено"
        for task in self.tasks:
            if task.status != "Завершено":
                status = "В роботі"
                break
        return status

    def get_data(self):
        return {
            "name": self.name,
            "deadline": self.deadline,
            "manager": self.manager,
            "tasks": [task.get_data() for task in self.tasks]
        }

# Клас Завдання
class Task:
    def __init__(self, description, deadline, status="Нова"):
        self.description = description
        self.deadline = deadline
        self.status = status

    def update_task(self, description, deadline, status):
        self.description = description
        self.deadline = deadline
        self.status = status

    def get_data(self):
        return {
            "description": self.description,
            "deadline": self.deadline,
            "status": self.status
        }

# Функції для додавання, оновлення та відстеження проектів
def add_project(name, deadline, manager):
    project = Project(name, deadline, manager)
    return project

def update_project(project, name, deadline, manager):
    project.name = name
    project.deadline = deadline
    project.manager = manager

def get_project_status(project):
    return project.get_status()

def print_project_data(project, project_id):
    print("Проект ID:", project_id)
    print("Назва проекту:", project.name)
    print("Термін виконання:", project.deadline)
    print("Відповідальний менеджер:", project.manager)
    print("Завдання:")
    for task_id, task in enumerate(project.tasks, start=1):
        print(f"    Завдання ID: {task_id}")
        print("        Опис:", task.description)
        print("        Термін виконання:", task.deadline)
        print("        Статус:", task.status)

# Функції для додавання та оновлення завдань
def add_task_to_project(project):
    description = input("Введіть опис завдання: ")
    deadline = input("Введіть термін виконання завдання: ")
    status = input("Введіть статус завдання (за замовчуванням 'Нова'): ") or "Нова"
    task = Task(description, deadline, status)
    project.add_task(task)
    print("Завдання успішно додане до проекту.")

def update_task_in_project(project):
    task_id = input("Введіть ідентифікатор завдання, яке потрібно оновити: ")
    try:
        task_id = int(task_id) - 1
        task = project.tasks[task_id]
    except (ValueError, IndexError):
        print("Невірний ідентифікатор завдання")
        return
    description = input("Введіть новий опис завдання: ")
    deadline = input("Введіть новий термін виконання завдання: ")
    status = input("Введіть новий статус завдання: ")
    task.update_task(description, deadline, status)
    print("Завдання успішно оновлене.")

# Функції для роботи з консоллю
def save_projects_to_json(projects, filename="projects.json"):
    data = [project.get_data() for project in projects]
    with open(filename, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def load_projects_from_json(filename="projects.json"):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            projects = [Project(project["name"], project["deadline"], project["manager"],
                                [Task(task["description"], task["deadline"], task["status"]) for task in project["tasks"]])
                        for project in data]
            return projects
    except FileNotFoundError:
        return []

def main():
    projects = load_projects_from_json()
    while True:
        print("Виберіть дію:")
        print("1. Додати проект")
        print("2. Оновити проект")
        print("3. Додати завдання до проекту")
        print("4. Оновити завдання у проекті")
        print("5. Видалити проект")
        print("6. Вивести список проектів")
        print("7. Зберегти та вийти")
        choice = input("Введіть номер дії: ")
        if choice == "1":
            project = add_project(input("Введіть назву проекту: "),
                                  input("Введіть термін виконання проекту: "),
                                  input("Введіть ім'я відповідального менеджера: "))
            projects.append(project)
        elif choice == "2":
            project_id = input("Введіть ідентифікатор проекту, який потрібно оновити: ")
            try:
                project = projects[int(project_id) - 1]
            except (ValueError, IndexError):
                print("Невірний ідентифікатор проекту")
                continue
            name = input("Введіть нову назву проекту: ")
            deadline = input("Введіть новий термін виконання проекту: ")
            manager = input("Введіть нове ім'я відповідального менеджера: ")
            update_project(project, name, deadline, manager)
        elif choice == "3":
            project_id = input("Введіть ідентифікатор проекту, до якого потрібно додати завдання: ")
            try:
                project = projects[int(project_id) - 1]
            except (ValueError, IndexError):
                print("Невірний ідентифікатор проекту")
                continue
            add_task_to_project(project)
        elif choice == "4":
            project_id = input("Введіть ідентифікатор проекту, у якому потрібно оновити завдання: ")
            try:
                project = projects[int(project_id) - 1]
            except (ValueError, IndexError):
                print("Невірний ідентифікатор проекту")
                continue
            update_task_in_project(project)
        elif choice == "5":
            project_id = input("Введіть ідентифікатор проекту, який потрібно видалити: ")
            try:
                projects.pop(int(project_id) - 1)
            except (ValueError, IndexError):
                print("Невірний ідентифікатор проекту")
                continue
        elif choice == "6":
            for project_id, project in enumerate(projects, start=1):
                print_project_data(project, project_id)
        elif choice == "7":
            save_projects_to_json(projects)
            break

if __name__ == "__main__":
    main()
