import logging
import time
from datetime import datetime
from typing import Optional, Dict, List

import grpc
from sqlalchemy.orm import Session
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from opentelemetry import trace

from core.database import SessionLocal
from core.models import Task
from core.services import TaskService
import task_pb2, task_pb2_grpc
from metrics import grpc_request_counter, grpc_request_latency

# Logging configuration
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def datetime_to_timestamp(dt: datetime) -> Timestamp:
    """Convert datetime object to Protocol Buffer Timestamp."""
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

class TaskServicer(task_pb2_grpc.TaskServiceServicer):
    """Task service implementation"""

    def __init__(self):
        self.db: Session = SessionLocal()

    def CreateTask(self, request, context):
        try:
            with grpc_request_latency.labels(method="CreateTask").time():
                task = TaskService.create_task(
                    db=self.db,
                    title=request.title,
                    description=request.description
                )
                grpc_request_counter.labels(method="CreateTask", status="success").inc()
                return task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at) if task.updated_at else None
                )
        except Exception as e:
            grpc_request_counter.labels(method="CreateTask", status="error").inc()
            logger.error(f"Error creating task: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return task_pb2.TaskResponse()

    def GetTask(self, request, context):
        try:
            with grpc_request_latency.labels(method="GetTask").time():
                task = TaskService.get_task(db=self.db, task_id=request.task_id)
                if not task:
                    grpc_request_counter.labels(method="GetTask", status="not_found").inc()
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with ID {request.task_id} not found")
                    return task_pb2.TaskResponse()
                
                grpc_request_counter.labels(method="GetTask", status="success").inc()
                return task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at) if task.updated_at else None
                )
        except Exception as e:
            grpc_request_counter.labels(method="GetTask", status="error").inc()
            logger.error(f"Error getting task: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return task_pb2.TaskResponse()

    def ListTasks(self, request, context):
        try:
            with grpc_request_latency.labels(method="ListTasks").time():
                skip = request.skip if request.skip else 0
                limit = request.limit if request.limit else 100
                tasks = TaskService.get_tasks(db=self.db, skip=skip, limit=limit)
                grpc_request_counter.labels(method="ListTasks", status="success").inc()
                return task_pb2.ListTasksResponse(
                    tasks=[
                        task_pb2.TaskResponse(
                            id=task.id,
                            title=task.title,
                            description=task.description,
                            completed=task.completed,
                            created_at=datetime_to_timestamp(task.created_at),
                            updated_at=datetime_to_timestamp(task.updated_at) if task.updated_at else None
                        )
                        for task in tasks
                    ]
                )
        except Exception as e:
            grpc_request_counter.labels(method="ListTasks", status="error").inc()
            logger.error(f"Error listing tasks: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return task_pb2.ListTasksResponse()

    def UpdateTask(self, request, context):
        with tracer.start_as_current_span("UpdateTask") as span:
            try:
                task = TaskService.update_task(
                    db=self.db,
                    task_id=request.task_id,
                    title=request.title if request.HasField("title") else None,
                    description=request.description if request.HasField("description") else None,
                    completed=request.completed if request.HasField("completed") else None
                )
                if task is None:
                    grpc_request_counter.labels(method="UpdateTask", status="not_found").inc()
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with id {request.task_id} not found")
                    return task_pb2.TaskResponse()
            
                grpc_request_counter.labels(method="UpdateTask", status="success").inc()
                return task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at) if task.updated_at else None
                )
            except Exception as e:
                grpc_request_counter.labels(method="UpdateTask", status="error").inc()
                logger.error(f"Error updating task: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return task_pb2.TaskResponse()

    def DeleteTask(self, request, context):
        with tracer.start_as_current_span("DeleteTask") as span:
            try:
                success = TaskService.delete_task(db=self.db, task_id=request.task_id)
                if not success:
                    grpc_request_counter.labels(method="DeleteTask", status="not_found").inc()
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with id {request.task_id} not found")
                    return task_pb2.DeleteTaskResponse(success=False)
            
                grpc_request_counter.labels(method="DeleteTask", status="success").inc()
                return task_pb2.DeleteTaskResponse(success=True)
            except Exception as e:
                grpc_request_counter.labels(method="DeleteTask", status="error").inc()
                logger.error(f"Error deleting task: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return task_pb2.DeleteTaskResponse(success=False)

    def WatchTasks(self, request, context):
        with tracer.start_as_current_span("WatchTasks") as span:
            try:
                tasks = TaskService.get_tasks(db=self.db)
                grpc_request_counter.labels(method="WatchTasks", status="success").inc()
                for task in tasks:
                    yield task_pb2.TaskResponse(
                        task=task_pb2.Task(
                            id=task.id,
                            title=task.title,
                            description=task.description,
                            completed=task.completed,
                            created_at=datetime_to_timestamp(task.created_at),
                            updated_at=datetime_to_timestamp(task.updated_at) if task.updated_at else None
                        )
                    )
            except Exception as e:
                grpc_request_counter.labels(method="WatchTasks", status="error").inc()
                logger.error(f"Error watching tasks: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return 