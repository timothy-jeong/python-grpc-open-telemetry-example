from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas import TaskCreate, Task, TaskUpdate
from core.services import TaskService

app = FastAPI(title="Task API", version="1.0.0")

# Prometheus 메트릭 설정
Instrumentator().instrument(app).expose(app)

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """새로운 태스크를 생성합니다."""
    return TaskService.create_task(db=db, title=task.title, description=task.description)

@app.get("/tasks/", response_model=List[Task])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """태스크 목록을 조회합니다."""
    return TaskService.get_tasks(db=db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """특정 태스크를 조회합니다."""
    task = TaskService.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """태스크를 업데이트합니다."""
    task = TaskService.update_task(
        db=db,
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        completed=task_update.completed
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """태스크를 삭제합니다."""
    success = TaskService.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
