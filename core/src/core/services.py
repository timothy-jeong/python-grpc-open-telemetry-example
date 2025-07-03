"""Business logic services."""
from typing import List, Optional

from sqlalchemy.orm import Session

from .models import Task
from .schemas import TaskCreate, TaskUpdate


class TaskService:
    """Task service class containing business logic for task operations."""

    @staticmethod
    def create_task(db: Session, title: str, description: str) -> Task:
        """Create a new task."""
        task = Task(title=title, description=description)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        """Retrieve a list of tasks."""
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        """Retrieve a specific task."""
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """Update a task."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """Delete a task."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        db.delete(task)
        db.commit()
        return True 