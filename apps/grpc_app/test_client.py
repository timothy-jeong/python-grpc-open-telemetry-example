import logging

import grpc
import logfire
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

import task_pb2
import task_pb2_grpc

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Logfire configuration
logfire.configure()

# gRPC client instrumentation
GrpcInstrumentorClient().instrument()

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = task_pb2_grpc.TaskServiceStub(channel)
        
        logfire.info("Starting gRPC client test")
        
        # Create task
        create_request = task_pb2.CreateTaskRequest(
            title="Test Task from gRPC Client",
            description="This is a test task created via gRPC"
        )
        
        logfire.info("Creating task", title=create_request.title)
        create_response = stub.CreateTask(create_request)
        logfire.info("Task created", task_id=create_response.id, title=create_response.title)
        
        task_id = create_response.id
        
        # Get task
        get_request = task_pb2.GetTaskRequest(task_id=task_id)
        logfire.info("Getting task", task_id=task_id)
        get_response = stub.GetTask(get_request)
        logfire.info("Task retrieved", task_id=get_response.id, title=get_response.title)
        
        # List tasks
        list_request = task_pb2.ListTasksRequest(skip=0, limit=10)
        logfire.info("Listing tasks")
        list_response = stub.ListTasks(list_request)
        logfire.info("Tasks listed", count=len(list_response.tasks))
        
        # Update task
        update_request = task_pb2.UpdateTaskRequest(
            task_id=task_id,
            title="Updated Test Task",
            description="This task has been updated"
        )
        logfire.info("Updating task", task_id=task_id, title=update_request.title)
        update_response = stub.UpdateTask(update_request)
        logfire.info("Task updated", task_id=update_response.id, title=update_response.title)
        
        # Delete task
        delete_request = task_pb2.DeleteTaskRequest(task_id=task_id)
        logfire.info("Deleting task", task_id=task_id)
        delete_response = stub.DeleteTask(delete_request)
        logfire.info("Task deleted", task_id=task_id, success=delete_response.success)
        
        logfire.info("gRPC client test completed successfully")

if __name__ == "__main__":
    run() 