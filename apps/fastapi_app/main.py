from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logfire
from sqlalchemy.orm import Session

from core.database import get_db, Base, engine
from core.schemas import TaskCreate, Task, TaskUpdate
from core.services import TaskService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API", version="1.0.0")

# Logfire configuration
logfire.configure()
logfire.instrument_fastapi(app)

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    logfire.info("Creating new task", title=task.title, description=task.description)
    result = TaskService.create_task(db=db, title=task.title, description=task.description)
    logfire.info("Task created successfully", task_id=result.id)
    return result

@app.get("/tasks/", response_model=List[Task])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of tasks."""
    logfire.info("Listing tasks", skip=skip, limit=limit)
    tasks = TaskService.get_tasks(db=db, skip=skip, limit=limit)
    logfire.info("Tasks listed successfully", count=len(tasks))
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task."""
    logfire.info("Getting task", task_id=task_id)
    task = TaskService.get_task(db=db, task_id=task_id)
    if task is None:
        logfire.warning("Task not found", task_id=task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logfire.info("Task retrieved successfully", task_id=task.id)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task."""
    logfire.info("Updating task", task_id=task_id, title=task_update.title, description=task_update.description)
    task = TaskService.update_task(
        db=db,
        task_id=task_id,
        title=task_update.title,
        description=task_update.description
    )
    if task is None:
        logfire.warning("Task not found for update", task_id=task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logfire.info("Task updated successfully", task_id=task.id)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    logfire.info("Deleting task", task_id=task_id)
    success = TaskService.delete_task(db=db, task_id=task_id)
    if not success:
        logfire.warning("Task not found for deletion", task_id=task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logfire.info("Task deleted successfully", task_id=task_id)
    return {"message": "Task deleted successfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
