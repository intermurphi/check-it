from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from db import init_db
from core import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from models import Task

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", 
                   "http://127.0.0.1:5173", 
                   "http://localhost:5174"
                   ],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
