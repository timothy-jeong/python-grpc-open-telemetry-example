import logging
from concurrent import futures
import threading

import grpc
import logfire
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

from task_servicer import TaskServicer
import task_pb2_grpc

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Logfire configuration
logfire.configure()

# gRPC server instrumentation
grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()

def serve():
    """Start the gRPC server"""
    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add TaskServicer to server
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskServicer(), server)
    
    # Listen on port 50051
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    
    logger.info(f"Starting gRPC server on {listen_addr}")
    logfire.info(f"Starting gRPC server on {listen_addr}")
    
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server...")
        logfire.info("Shutting down gRPC server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
