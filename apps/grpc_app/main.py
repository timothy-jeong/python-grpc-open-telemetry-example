import logging
from concurrent import futures
import threading

import grpc
from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PrometheusMetricReader
from prometheus_client import start_http_server

from core.database import create_tables
from task_servicer import TaskServicer
import task_pb2_grpc

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenTelemetry configuration
trace.set_tracer_provider(TracerProvider())

# Add Console Exporter (for development)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Prometheus metrics configuration
prometheus_reader = PrometheusMetricReader()
meter_provider = MeterProvider(metric_readers=[prometheus_reader])

# gRPC server instrumentation
grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()

def start_prometheus_server():
    # Start Prometheus metrics server
    start_http_server(50052)
    logger.info("Prometheus metrics server started on port 50052")

def serve():
    # Create database tables
    create_tables()
    
    # gRPC server configuration
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register Task service
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskServicer(), server)
    
    # Start server
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    # Start Prometheus server in background
    prometheus_thread = threading.Thread(target=start_prometheus_server)
    prometheus_thread.daemon = True
    prometheus_thread.start()
    
    server.start()
    logger.info("gRPC server started on port 50051")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        server.stop(0)

if __name__ == '__main__':
    serve()
