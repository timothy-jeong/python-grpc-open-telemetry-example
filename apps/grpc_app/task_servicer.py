from datetime import datetime
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.orm import Session

from core.database import get_db
from core.services import TaskService
import task_pb2
import task_pb2_grpc


def datetime_to_timestamp(dt: Optional[datetime]) -> Optional[Timestamp]:
    """datetime 객체를 Protocol Buffer Timestamp로 변환합니다."""
    if dt is None:
        return None
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


class TaskServicer(task_pb2_grpc.TaskServiceServicer):
    """Task 서비스 구현체"""

    def __init__(self):
        self._db = next(get_db())

    def CreateTask(self, request, context):
        """태스크를 생성합니다."""
        task = TaskService.create_task(
            db=self._db,
            title=request.title,
            description=request.description if request.HasField("description") else None
        )
        return self._task_to_proto(task)

    def ListTasks(self, request, context):
        """태스크 목록을 조회합니다."""
        tasks = TaskService.get_tasks(
            db=self._db,
            skip=request.skip,
            limit=request.limit
        )
        return task_pb2.ListTasksResponse(
            tasks=[self._task_to_proto(task) for task in tasks]
        )

    def GetTask(self, request, context):
        """특정 태스크를 조회합니다."""
        task = TaskService.get_task(db=self._db, task_id=request.task_id)
        if task is None:
            context.abort(404, "Task not found")
        return self._task_to_proto(task)

    def UpdateTask(self, request, context):
        """태스크를 업데이트합니다."""
        task = TaskService.update_task(
            db=self._db,
            task_id=request.task_id,
            title=request.title if request.HasField("title") else None,
            description=request.description if request.HasField("description") else None,
            completed=request.completed if request.HasField("completed") else None
        )
        if task is None:
            context.abort(404, "Task not found")
        return self._task_to_proto(task)

    def DeleteTask(self, request, context):
        """태스크를 삭제합니다."""
        success = TaskService.delete_task(db=self._db, task_id=request.task_id)
        if not success:
            context.abort(404, "Task not found")
        return task_pb2.DeleteTaskResponse(success=True)

    def _task_to_proto(self, task) -> task_pb2.TaskResponse:
        """Task 모델을 Protocol Buffer 메시지로 변환합니다."""
        response = task_pb2.TaskResponse(
            id=task.id,
            title=task.title,
            completed=task.completed,
            created_at=datetime_to_timestamp(task.created_at)
        )
        
        if task.description:
            response.description = task.description
        
        if task.updated_at:
            response.updated_at.CopyFrom(datetime_to_timestamp(task.updated_at))
        
        return response 