import logging

import grpc
from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

import task_pb2
import task_pb2_grpc

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenTelemetry configuration
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# gRPC client instrumentation
grpc_client_instrumentor = GrpcInstrumentorClient()
grpc_client_instrumentor.instrument()

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = task_pb2_grpc.TaskServiceStub(channel)
        
        # Create task
        create_request = task_pb2.CreateTaskRequest(
            title="Test Task",
            description="This is a task for OpenTelemetry testing."
        )
        create_response = stub.CreateTask(create_request)
        logger.info(f"Created task ID: {create_response.id}")
        logger.info(f"Created task title: {create_response.title}")
        
        # Get task
        get_request = task_pb2.GetTaskRequest(task_id=create_response.id)
        get_response = stub.GetTask(get_request)
        logger.info(f"Retrieved task: ID={get_response.id}, title={get_response.title}")
        
        # List tasks
        list_request = task_pb2.ListTasksRequest()
        list_response = stub.ListTasks(list_request)
        logger.info(f"Total number of tasks: {len(list_response.tasks)}")
        
        # Print each task information
        for i, task in enumerate(list_response.tasks):
            logger.info(f"Task {i+1}: ID={task.id}, title={task.title}")

if __name__ == "__main__":
    run() 