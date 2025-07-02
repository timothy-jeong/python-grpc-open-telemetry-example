from datetime import datetime
from typing import Optional, Dict, List

from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.orm import Session

from core.database import get_db_context
from core.services import TaskService
import task_pb2
import task_pb2_grpc
from open_telemetry_exporter import OTelMetricExporter

# 메트릭 수집을 위한 전역 딕셔너리
all_metrics: Dict[str, List] = {}

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
        # OpenTelemetry 메트릭 익스포터 초기화
        self._metric_exporter = OTelMetricExporter(
            all_metrics=all_metrics,
            print_live=True  # 실시간으로 메트릭 출력
        )

    def _record_metric(self, metric_name: str, attributes: Dict = None):
        """메트릭을 기록합니다."""
        if attributes is None:
            attributes = {}
        
        # 메트릭 이름이 없으면 초기화
        if metric_name not in all_metrics:
            all_metrics[metric_name] = []
        
        # 메트릭 기록
        all_metrics[metric_name].append(attributes)

    def CreateTask(self, request, context):
        """태스크를 생성합니다."""
        try:
            with get_db_context() as db:
                task = TaskService.create_task(
                    db=db,
                    title=request.title,
                    description=request.description if request.HasField("description") else None
                )
            
                # 성공 메트릭 기록
                self._record_metric(
                    "task.create.success",
                    {"method": "CreateTask", "task_id": str(task.id)}
                )
            
                return self._task_to_proto(task)
        except Exception as e:
            # 실패 메트릭 기록
            self._record_metric(
                "task.create.error",
                {"method": "CreateTask", "error": str(e)}
            )
            raise

    def ListTasks(self, request, context):
        """태스크 목록을 조회합니다."""
        try:
            with get_db_context() as db:
                tasks = TaskService.get_tasks(
                    db=db,
                    skip=request.skip,
                    limit=request.limit
                )
            
                # 성공 메트릭 기록
                self._record_metric(
                    "task.list.success",
                    {"method": "ListTasks", "count": len(tasks)}
                )
            
                return task_pb2.ListTasksResponse(
                    tasks=[self._task_to_proto(task) for task in tasks]
                )
        except Exception as e:
            # 실패 메트릭 기록
            self._record_metric(
                "task.list.error",
                {"method": "ListTasks", "error": str(e)}
            )
            raise

    def GetTask(self, request, context):
        """특정 태스크를 조회합니다."""
        try:
            with get_db_context() as db:
                task = TaskService.get_task(db=db, task_id=request.task_id)
                if task is None:
                    # 실패 메트릭 기록
                    self._record_metric(
                        "task.get.not_found",
                        {"method": "GetTask", "task_id": str(request.task_id)}
                    )
                    context.abort(404, "Task not found")
            
                # 성공 메트릭 기록
                self._record_metric(
                    "task.get.success",
                    {"method": "GetTask", "task_id": str(task.id)}
                )
            
                return self._task_to_proto(task)
        except Exception as e:
            # 실패 메트릭 기록
            self._record_metric(
                "task.get.error",
                {"method": "GetTask", "error": str(e)}
            )
            raise

    def UpdateTask(self, request, context):
        """태스크를 업데이트합니다."""
        try:
            with get_db_context() as db:
                task = TaskService.update_task(
                    db=db,
                    task_id=request.task_id,
                    title=request.title if request.HasField("title") else None,
                    description=request.description if request.HasField("description") else None,
                    completed=request.completed if request.HasField("completed") else None
                )
                if task is None:
                    # 실패 메트릭 기록
                    self._record_metric(
                        "task.update.not_found",
                        {"method": "UpdateTask", "task_id": str(request.task_id)}
                    )
                    context.abort(404, "Task not found")
            
                # 성공 메트릭 기록
                self._record_metric(
                    "task.update.success",
                    {"method": "UpdateTask", "task_id": str(task.id)}
                )
            
                return self._task_to_proto(task)
        except Exception as e:
            # 실패 메트릭 기록
            self._record_metric(
                "task.update.error",
                {"method": "UpdateTask", "error": str(e)}
            )
            raise

    def DeleteTask(self, request, context):
        """태스크를 삭제합니다."""
        try:
            with get_db_context() as db:
                success = TaskService.delete_task(db=db, task_id=request.task_id)
                if not success:
                    # 실패 메트릭 기록
                    self._record_metric(
                        "task.delete.not_found",
                        {"method": "DeleteTask", "task_id": str(request.task_id)}
                    )
                    context.abort(404, "Task not found")
            
                # 성공 메트릭 기록
                self._record_metric(
                    "task.delete.success",
                    {"method": "DeleteTask", "task_id": str(request.task_id)}
                )
            
                return task_pb2.DeleteTaskResponse(success=True)
        except Exception as e:
            # 실패 메트릭 기록
            self._record_metric(
                "task.delete.error",
                {"method": "DeleteTask", "error": str(e)}
            )
            raise

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