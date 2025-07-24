import argparse
import requests

BASE_URL = "http://localhost:3000/api/v1/tasks"

def list_tasks():
    response = requests.get(BASE_URL)
    tasks = response.json()
    for task in tasks:
        status = "✅" if task["completed"] else "❌"
        print(f'{task["id"]}: {task["title"]} - {status}')

def add_task(title):
    payload = {
        "task": {
            "title": title,
            "description": "",
            "completed": False
        }
    }
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print("Task added successfully.")
    else:
        print("Failed to add task:", response.text)

def complete_task(task_id):
    payload = {
        "task": {
            "completed": True
        }
    }
    response = requests.patch(f"{BASE_URL}/{task_id}", json=payload)
    if response.ok:
        print("Task marked as completed.")
    else:
        print("Failed to update task:", response.text)

def delete_task(task_id):
    response = requests.delete(f"{BASE_URL}/{task_id}")
    if response.ok:
        print("Task deleted.")
    else:
        print("Failed to delete task:", response.text)

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # task list
    subparsers.add_parser("list", help="List all tasks")

    # task add "title"
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")

    # task complete <id>
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # task delete <id>
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "list":
        list_tasks()
    elif args.command == "add":
        add_task(args.title)
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

