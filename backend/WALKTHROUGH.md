# Task Manager API - Implementation Walkthrough

This guide will walk you through building a simple Task Manager API using FastAPI and SQLite from scratch.

## Prerequisites

- Python 3.7 or higher
- Basic understanding of REST APIs
- Terminal/Command line knowledge

## Step 1: Project Setup

Create a new directory for your project:

```bash
mkdir task-manager-api
cd task-manager-api
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 2: Install Dependencies

Create a `requirements.txt` file with the following content:

```
fastapi
uvicorn[standard]
pydantic
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Step 3: Create the Data Model

Create a file named `models.py`:

```python
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    desc: str
    status: bool
```

This defines the structure of a Task object with:
- `id`: Unique identifier
- `name`: Task name
- `desc`: Task description
- `status`: Completion status (True/False)

## Step 4: Set Up the Database

Create a file named `db.py`:

```python
import sqlite3

DATABASE_NAME = "tasks.db"

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            desc TEXT NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
```

This module handles:
- Database connection management
- Table creation on startup

## Step 5: Implement Business Logic

Create a file named `core.py`:

```python
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
```

This module contains all CRUD operations:
- **Create**: Add new tasks
- **Read**: Get all tasks or a specific task
- **Update**: Modify existing tasks
- **Delete**: Remove tasks

## Step 6: Create the API

Create a file named `main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from db import init_db
from core import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from models import Task

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Request models
class TaskCreate(BaseModel):
    name: str
    desc: str
    status: bool = False

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    status: Optional[bool] = None

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Task Manager API"}

@app.post("/tasks", response_model=Task)
def create_new_task(task: TaskCreate):
    """Create a new task."""
    return create_task(name=task.name, desc=task.desc, status=task.status)

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Get all tasks."""
    return get_all_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a specific task by ID."""
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task_update: TaskUpdate):
    """Update a task."""
    task = update_task(task_id, name=task_update.name, desc=task_update.desc, status=task_update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int):
    """Delete a task."""
    deleted = delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
```

## Step 7: Run the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

## Step 8: Test the API

### Using curl:

**Get the welcome message:**
```bash
curl http://127.0.0.1:8000/
```

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"name":"Buy groceries","desc":"Milk, eggs, bread","status":false}'
```

**Get all tasks:**
```bash
curl http://127.0.0.1:8000/tasks
```

**Get a specific task:**
```bash
curl http://127.0.0.1:8000/tasks/1
```

**Update a task:**
```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":true}'
```

**Delete a task:**
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

### Using the Interactive API Docs:

Visit `http://127.0.0.1:8000/docs` in your browser to access FastAPI's built-in interactive documentation (Swagger UI). You can test all endpoints directly from the browser.

## Project Structure

Your final project structure should look like this:

```
task-manager-api/
├── venv/                 # Virtual environment
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic data models
├── core.py              # Business logic (CRUD operations)
├── db.py                # Database setup and connection
├── requirements.txt     # Project dependencies
└── tasks.db            # SQLite database (created automatically)
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Key Concepts Explained

### FastAPI
- Modern Python web framework for building APIs
- Automatic API documentation
- Type hints for data validation
- Async support (though not used in this simple example)

### Pydantic
- Data validation using Python type hints
- Automatic request/response serialization
- Clear error messages for invalid data

### SQLite
- Lightweight, file-based database
- No separate server required
- Perfect for small to medium applications
- Data persists in `tasks.db` file

### CRUD Operations
- **Create**: POST to add new resources
- **Read**: GET to retrieve resources
- **Update**: PUT to modify existing resources
- **Delete**: DELETE to remove resources

## Next Steps and Enhancements

Once you're comfortable with the basics, consider adding:

1. **Authentication**: Add user login and JWT tokens
2. **Task Categories**: Organize tasks into categories
3. **Due Dates**: Add deadline tracking
4. **Priority Levels**: Mark tasks as high/medium/low priority
5. **Search and Filter**: Find tasks by name, status, or date
6. **PostgreSQL**: Switch to a production-ready database
7. **Frontend**: Build a React or Vue.js interface
8. **Docker**: Containerize the application
9. **Tests**: Add unit and integration tests
10. **Deployment**: Deploy to services like Heroku, AWS, or DigitalOcean

## Troubleshooting

**Port already in use:**
```bash
uvicorn main:app --reload --port 8001
```

**Module not found errors:**
Make sure your virtual environment is activated and dependencies are installed.

**Database locked:**
Close any other connections to the database or restart the server.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [REST API Design Best Practices](https://restfulapi.net/)

Happy coding!
