# ===== Importing external modules =====
import datetime
import os


# ===== User Functions =====

def read_users():
    """
    Read user credentials from 'user.txt'.
    Returns a dictionary of username-password pairs.
    """
    users = {}
    try:
        with open("user.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(", ")
                users[username] = password
    except FileNotFoundError:
        print("No user.txt file found.")
    return users


def write_user(username, password):
    """
    Append a new username and password to 'user.txt'.
    """
    with open("user.txt", "a") as file:
        file.write(f"{username}, {password}\n")


def reg_user(users):
    """
    Register a new user after validating inputs.
    """
    new_username = input("Enter new username: ").strip()
    if not new_username:
        print("Username cannot be empty.")
        return

    if new_username in users:
        print("Username already exists.")
        return

    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm password: ").strip()

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    write_user(new_username, new_password)
    users[new_username] = new_password
    print("User registered successfully.")


# ===== Task Functions =====

def add_task(logged_in_user):
    """
    Add a new task to 'task.txt'.
    Validate required fields before saving.
    """
    assigned_user = input("Enter username to assign task: ").strip()
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    due_date = input("Enter due date (e.g. 12 May 2025): ").strip()

    if not (assigned_user and title and description and due_date):
        print("All fields are required.")
        return

    try:
        datetime.datetime.strptime(due_date, "%d %b %Y")
    except ValueError:
        print("Invalid date format. Use 'dd Mon YYYY'.")
        return

    date_assigned = datetime.datetime.now().strftime("%d %b %Y")

    with open("task.txt", "a") as file:
        file.write(
            f"\n{assigned_user}, {title}, {description}, {due_date}, "
            f"{date_assigned}, No"
        )
    print("Task added successfully.")


def view_all_task():
    """
    Display all tasks from 'task.txt'.
    """
    try:
        with open("task.txt", "r") as file:
            for line in file:
                (username, title, description, due_date,
                 created_date, completed) = line.strip().split(", ")
                print(f"Assigned to: {username}\nTitle: {title}\n"
                      f"Description: {description}\nDue: {due_date}\n"
                      f"Created: {created_date}\nCompleted: {completed}\n")
    except FileNotFoundError:
        print("No tasks found.")


def view_mine(username):
    """
    Display and optionally edit or complete tasks assigned
    to the current user.
    """
    tasks = []
    try:
        with open("task.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("No tasks found.")
        return

    for i, line in enumerate(lines):
        task_username, title, description, due_date, created_date, completed = line.strip().split(", ")
        tasks.append((i, task_username, title, description,
                          due_date, created_date, completed))
        if task_username == username:
            print(f"{i + 1}. Title: {title}\n   Description: {description}\n"
                  f"   Due: {due_date}\n   Created: {created_date}\n"
                  f"   Completed: {completed}\n")

    if not tasks:
        print("No personal tasks found.")
        return

    task_number = input("Enter task number to edit/mark complete "
                        "or -1 to return: ").strip()
    if task_number == "-1":
        return

    try:
        index = int(task_number) - 1
        print(index)
        task_line_index, _, title, _, _, _, completed = tasks[index]

        if completed.lower() == "yes":
            print("Task already completed.")
            return

        action = input("Mark as (c)omplete or (e)dit? ").lower().strip()
        if action == "c":
            mark_task_complete(task_line_index, lines)
        elif action == "e":
            edit_task(task_line_index, lines)
        else:
            print("Invalid action.")
    except (IndexError, ValueError):
        print("Invalid task number.")


def mark_task_complete(index, lines):
    """
    Mark the specified task as completed.
    """
    parts = lines[index].strip().split(", ")
    parts[-1] = "Yes"
    lines[index] = ", ".join(parts) + "\n"
    with open("task.txt", "w") as file:
        file.writelines(lines)
    print("Task marked complete.")


def edit_task(index, lines):
    """
    Edit the assigned user or due date of a task.
    """
    parts = lines[index].strip().split(", ")
    new_user = input("New username (leave blank to keep current): ").strip()
    new_due_date = input("New due date (leave blank to keep current): ").strip()

    if new_user:
        parts[0] = new_user
    if new_due_date:
        try:
            datetime.datetime.strptime(new_due_date, "%d %b %Y")
            parts[3] = new_due_date
        except ValueError:
            print("Invalid date format. Use 'dd Mon YYYY'.")
            return

    lines[index] = ", ".join(parts) + "\n"
    with open("task.txt", "w") as file:
        file.writelines(lines)
    print("Task updated.")


def view_completed_task():
    """
    Display all completed tasks.
    """
    try:
        with open("task.txt", "r") as file:
            for line in file:
                (username, title, description, due_date,
                 created_date, completed) = line.strip().split(", ")
                if completed.lower() == "yes":
                    print(f"Assigned to: {username}\nTitle: {title}\n"
                          f"Description: {description}\nDue: {due_date}\n"
                          f"Created: {created_date}\n")
    except FileNotFoundError:
        print("No tasks found.")


def delete_task():
    """
    Delete a task by its title.
    """
    title_to_delete = input("Enter title of task to delete: ").strip()
    task_found = False

    try:
        with open("task.txt", "r") as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("No tasks found.")
        return

    with open("task.txt", "w") as file:
        for task in tasks:
            if title_to_delete not in task:
                file.write(task)
            else:
                task_found = True

    if task_found:
        print("Task deleted.")
    else:
        print("Task not found.")


# ===== Report Functions =====

def generate_reports():
    """
    Generate summary reports for tasks and users.
    """
    total, completed, uncompleted, overdue = 0, 0, 0, 0
    current_date = datetime.datetime.now().date()
    users = read_users()
    user_stats = {
        user: {"total": 0, "completed": 0, "overdue": 0}
        for user in users
    }

    try:
        with open("task.txt", "r") as file:
            for line in file:
                total += 1
                username, _, _, due_date, _, completed_flag = (
                    line.strip().split(", ")
                )
                due = datetime.datetime.strptime(due_date, "%d %b %Y").date()

                if completed_flag.lower() == "yes":
                    completed += 1
                    user_stats[username]["completed"] += 1
                else:
                    uncompleted += 1
                    if due < current_date:
                        overdue += 1
                        user_stats[username]["overdue"] += 1

                user_stats[username]["total"] += 1

        with open("task_overview.txt", "w") as file:
            file.write(f"Total tasks: {total}\nCompleted: {completed}\n"
                       f"Uncompleted: {uncompleted}\nOverdue: {overdue}\n"
                       f"Incomplete %: {uncompleted / total * 100:.2f}%\n"
                       f"Overdue %: {overdue / total * 100:.2f}%\n")

        with open("user_overview.txt", "w") as file:
            file.write(f"Total users: {len(users)}\n")
            file.write(f"Total tasks: {total}\n")
            for user, stats in user_stats.items():
                percent = lambda val: (
                    val / stats["total"] * 100 if stats["total"] > 0 else 0
                )
                file.write(
                    f"\nUser: {user}\nTasks: {stats['total']}\n"
                    f"Completed: {percent(stats['completed']):.2f}%\n"
                    f"Overdue: {percent(stats['overdue']):.2f}%\n"
                )

        print("Reports generated.")
    except FileNotFoundError:
        print("task.txt not found.")


def display_statistics():
    """
    Display task and user statistics. Generate reports if needed.
    """
    if not os.path.exists("task_overview.txt") or \
       not os.path.exists("user_overview.txt"):
        print("Generating reports first...")
        generate_reports()

    print("\n--- Task Overview ---")
    with open("task_overview.txt") as file:
        print(file.read())

    print("\n--- User Overview ---")
    with open("user_overview.txt") as file:
        print(file.read())

# ===== Main Program =====


users = read_users()
logged_in_user = ""

# Login loop
while not logged_in_user:
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in users and users[username] == password:
        logged_in_user = username
        print(f"Welcome, {username}!")
    else:
        print("Invalid credentials.")

# Menu loop
while True:
    if logged_in_user == "admin":
        menu = input(
            "\nChoose:\n"
            "r - register user\n"
            "a - add task\n"
            "va - view all\n"
            "vm - view mine\n"
            "vc - view completed\n"
            "del - delete task\n"
            "ds - display stats\n"
            "gr - generate reports\n"
            "e - exit\n: "
        ).lower().strip()
    else:
        menu = input(
            "\nChoose:\n"
            "a - add task\n"
            "va - view all\n"
            "vm - view mine\n"
            "e - exit\n: "
        ).lower().strip()

    if menu == "r" and logged_in_user == "admin":
        reg_user(users)
    elif menu == "a":
        add_task(logged_in_user)
    elif menu == "va":
        view_all_task()
    elif menu == "vm":
        view_mine(logged_in_user)
    elif menu == "vc" and logged_in_user == "admin":
        view_completed_task()
    elif menu == "del" and logged_in_user == "admin":
        delete_task()
    elif menu == "gr" and logged_in_user == "admin":
        generate_reports()
    elif menu == "ds" and logged_in_user == "admin":
        display_statistics()
    elif menu == "e":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
