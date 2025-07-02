"""Business logic services."""
from typing import List, Optional

from sqlalchemy.orm import Session

from core.models import Task


class TaskService:
    """Task service for handling business logic."""

    @staticmethod
    def create_task(db: Session, title: str, description: Optional[str] = None) -> Task:
        """새로운 태스크를 생성합니다."""
        task = Task(title=title, description=description)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        """태스크 목록을 조회합니다."""
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        """특정 태스크를 조회합니다."""
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """태스크를 업데이트합니다."""
        task = TaskService.get_task(db, task_id)
        if task:
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
        """태스크를 삭제합니다."""
        task = TaskService.get_task(db, task_id)
        if task:
            db.delete(task)
            db.commit()
            return True
        return False 