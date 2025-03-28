import os
import sqlite3
import bcrypt
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress
import datetime
import json
import click
from rich.text import Text

console = Console()

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            due_date TEXT,
            priority INTEGER,
            status TEXT,
            tags TEXT,
            created_at TEXT,
            updated_at TEXT,
            archived INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return user[0]
    return None

def add_task(user_id, title, description, due_date, priority, tags):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, title, description, due_date, priority, status, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (user_id, title, description, due_date, priority, 'Pending', tags, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_tasks(user_id, archived=False):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id = ? AND archived = ?", (user_id, archived))
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def archive_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET archived = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def edit_task(task_id, title=None, description=None, due_date=None, priority=None, tags=None):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    task = get_task_by_id(task_id)
    updated_title = title if title else task[2]
    updated_description = description if description else task[3]
    updated_due_date = due_date if due_date else task[4]
    updated_priority = priority if priority else task[5]
    updated_tags = tags if tags else task[7]
    c.execute("UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ?, tags = ?, updated_at = ? WHERE id = ?",
              (updated_title, updated_description, updated_due_date, updated_priority, updated_tags, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id))
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def display_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("Due Date")
    table.add_column("Priority")
    table.add_column("Status")
    for task in tasks:
        table.add_row(str(task[0]), task[2], task[4], str(task[5]), task[6])
    console.print(table)

def filter_tasks_by_priority(tasks, priority_level):
    filtered_tasks = [task for task in tasks if task[5] == priority_level]
    display_tasks(filtered_tasks)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username')
@click.argument('password')
def signup(username, password):
    if authenticate_user(username, password) is not None:
        console.print("[bold red]User already exists[/]")
    else:
        create_user(username, password)
        console.print("[bold green]User created successfully![/]")

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    user_id = authenticate_user(username, password)
    if user_id:
        console.print(f"[bold green]Login successful! Welcome {username}[/]")
        show_user_tasks(user_id)
    else:
        console.print("[bold red]Invalid credentials[/]")

@cli.command()
@click.argument('title')
@click.argument('description')
@click.argument('due_date')
@click.argument('priority', type=int)
@click.argument('tags')
def add_new_task(title, description, due_date, priority, tags):
    user_id = Prompt.ask("Enter user id", type=int)
    add_task(user_id, title, description, due_date, priority, tags)
    console.print("[bold green]Task added successfully![/]")

def show_user_tasks(user_id):
    tasks = get_tasks(user_id)
    if tasks:
        display_tasks(tasks)
    else:
        console.print("[bold red]No tasks found[/]")

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    delete_task(task_id)
    console.print("[bold red]Task deleted[/]")

@cli.command()
@click.argument('task_id', type=int)
def archive(task_id):
    archive_task(task_id)
    console.print("[bold yellow]Task archived[/]")

@cli.command()
@click.argument('task_id', type=int)
def edit(task_id):
    title = Prompt.ask("Enter new title")
    description = Prompt.ask("Enter new description")
    due_date = Prompt.ask("Enter new due date")
    priority = Prompt.ask("Enter new priority", type=int)
    tags = Prompt.ask("Enter new tags")
    edit_task(task_id, title, description, due_date, priority, tags)
    console.print("[bold green]Task updated successfully![/]")

@cli.command()
@click.argument('priority_level', type=int)
def filter_priority(priority_level):
    user_id = Prompt.ask("Enter user id", type=int)
    tasks = get_tasks(user_id)
    filter_tasks_by_priority(tasks, priority_level)

if __name__ == "__main__":
    init_db()
    cli()
