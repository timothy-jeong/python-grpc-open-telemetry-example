import logging
import time
from datetime import datetime
from typing import Optional, Dict, List

import grpc
import logfire
from sqlalchemy.orm import Session
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from core.database import SessionLocal
from core.models import Task
from core.services import TaskService
import task_pb2, task_pb2_grpc
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

# Logging configuration
logger = logging.getLogger(__name__)

logfire.configure()
GrpcInstrumentorServer().instrument()

def datetime_to_timestamp(dt: datetime) -> Timestamp:
    """Convert datetime object to Protocol Buffer Timestamp."""
    if dt is None:
        # Return current time if dt is None
        dt = datetime.utcnow()
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

class TaskServicer(task_pb2_grpc.TaskServiceServicer):
    """Task service implementation"""

    def _get_db_session(self) -> Session:
        """Get database session"""
        return SessionLocal()

    def _record_request(self, method: str, status: str, duration: float):
        """Record request metrics with Logfire"""
        logfire.info(
            "gRPC request completed",
            method=method,
            status=status,
            duration_seconds=duration
        )

    def CreateTask(self, request, context):
        """Create a new task"""
        start_time = time.time()
        method = "CreateTask"
        
        try:
            with self._get_db_session() as db:
                logfire.info("Creating new task", title=request.title, description=request.description)
                
                task = TaskService.create_task(
                    db=db, 
                    title=request.title, 
                    description=request.description
                )
                
                response = task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at)
                )
                
                duration = time.time() - start_time
                self._record_request(method, "success", duration)
                
                logfire.info("Task created successfully", task_id=task.id, duration=duration)
                return response
                
        except Exception as e:
            duration = time.time() - start_time
            self._record_request(method, "error", duration)
            
            logfire.error("Failed to create task", error=str(e), duration=duration)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            raise

    def GetTask(self, request, context):
        """Get a specific task"""
        start_time = time.time()
        method = "GetTask"
        
        try:
            with self._get_db_session() as db:
                logfire.info("Getting task", task_id=request.task_id)
                
                task = TaskService.get_task(db=db, task_id=request.task_id)
                
                if not task:
                    duration = time.time() - start_time
                    self._record_request(method, "not_found", duration)
                    
                    logfire.warning("Task not found", task_id=request.task_id, duration=duration)
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with id {request.task_id} not found")
                    return task_pb2.TaskResponse()
                
                response = task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at)
                )
                
                duration = time.time() - start_time
                self._record_request(method, "success", duration)
                
                logfire.info("Task retrieved successfully", task_id=task.id, duration=duration)
                return response
                
        except Exception as e:
            duration = time.time() - start_time
            self._record_request(method, "error", duration)
            
            logfire.error("Failed to get task", task_id=request.task_id, error=str(e), duration=duration)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            raise

    def ListTasks(self, request, context):
        """List all tasks"""
        start_time = time.time()
        method = "ListTasks"
        
        try:
            with self._get_db_session() as db:
                logfire.info("Listing tasks", skip=request.skip, limit=request.limit)
                
                tasks = TaskService.get_tasks(db=db, skip=request.skip, limit=request.limit)
                
                task_responses = []
                for task in tasks:
                    task_response = task_pb2.TaskResponse(
                        id=task.id,
                        title=task.title,
                        description=task.description,
                        completed=task.completed,
                        created_at=datetime_to_timestamp(task.created_at),
                        updated_at=datetime_to_timestamp(task.updated_at)
                    )
                    task_responses.append(task_response)
                
                response = task_pb2.ListTasksResponse(tasks=task_responses)
                
                duration = time.time() - start_time
                self._record_request(method, "success", duration)
                
                logfire.info("Tasks listed successfully", count=len(tasks), duration=duration)
                return response
                
        except Exception as e:
            duration = time.time() - start_time
            self._record_request(method, "error", duration)
            
            logfire.error("Failed to list tasks", error=str(e), duration=duration)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            raise

    def UpdateTask(self, request, context):
        """Update a task"""
        start_time = time.time()
        method = "UpdateTask"
        
        try:
            with self._get_db_session() as db:
                logfire.info("Updating task", task_id=request.task_id, title=request.title, description=request.description)
                
                task = TaskService.update_task(
                    db=db,
                    task_id=request.task_id,
                    title=request.title,
                    description=request.description
                )
                
                if not task:
                    duration = time.time() - start_time
                    self._record_request(method, "not_found", duration)
                    
                    logfire.warning("Task not found for update", task_id=request.task_id, duration=duration)
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with id {request.task_id} not found")
                    return task_pb2.TaskResponse()
                
                response = task_pb2.TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=datetime_to_timestamp(task.created_at),
                    updated_at=datetime_to_timestamp(task.updated_at)
                )
                
                duration = time.time() - start_time
                self._record_request(method, "success", duration)
                
                logfire.info("Task updated successfully", task_id=task.id, duration=duration)
                return response
                
        except Exception as e:
            duration = time.time() - start_time
            self._record_request(method, "error", duration)
            
            logfire.error("Failed to update task", task_id=request.task_id, error=str(e), duration=duration)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            raise

    def DeleteTask(self, request, context):
        """Delete a task"""
        start_time = time.time()
        method = "DeleteTask"
        
        try:
            with self._get_db_session() as db:
                logfire.info("Deleting task", task_id=request.task_id)
                
                success = TaskService.delete_task(db=db, task_id=request.task_id)
                
                if not success:
                    duration = time.time() - start_time
                    self._record_request(method, "not_found", duration)
                    
                    logfire.warning("Task not found for deletion", task_id=request.task_id, duration=duration)
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Task with id {request.task_id} not found")
                    return task_pb2.DeleteTaskResponse(success=False)
                
                duration = time.time() - start_time
                self._record_request(method, "success", duration)
                
                logfire.info("Task deleted successfully", task_id=request.task_id, duration=duration)
                return task_pb2.DeleteTaskResponse(success=True)
                
        except Exception as e:
            duration = time.time() - start_time
            self._record_request(method, "error", duration)
            
            logfire.error("Failed to delete task", task_id=request.task_id, error=str(e), duration=duration)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            raise 