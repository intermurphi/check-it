from db import get_db_connection
from models import Task
from typing import List, Optional

def create_task(name: str, desc: str, status: bool = False) -> Task:
    """Create a new task in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO tasks (name, desc, status) VALUES (?, ?, ?)',
        (name, desc, status)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return Task(id=task_id, name=name, desc=desc, status=status)

def get_all_tasks() -> List[Task]:
    """Retrieve all tasks from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    return [Task(id=row['id'], name=row['name'], desc=row['desc'], status=bool(row['status'])) for row in rows]

def get_task_by_id(task_id: int) -> Optional[Task]:
    """Retrieve a specific task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Task(id=row['id'], name=row['name'], desc=row['desc'], status=bool(row['status']))
    return None

def update_task(task_id: int, name: str = None, desc: str = None, status: bool = None) -> Optional[Task]:
    """Update a task's fields."""
    task = get_task_by_id(task_id)
    if not task:
        return None

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update only provided fields
    updated_name = name if name is not None else task.name
    updated_desc = desc if desc is not None else task.desc
    updated_status = status if status is not None else task.status

    cursor.execute(
        'UPDATE tasks SET name = ?, desc = ?, status = ? WHERE id = ?',
        (updated_name, updated_desc, updated_status, task_id)
    )
    conn.commit()
    conn.close()

    return Task(id=task_id, name=updated_name, desc=updated_desc, status=updated_status)

def delete_task(task_id: int) -> bool:
    """Delete a task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted
