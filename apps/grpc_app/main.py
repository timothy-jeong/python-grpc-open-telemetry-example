import logging
from concurrent import futures

import grpc
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

from core.database import Base, engine
from apps.grpc_app import task_pb2_grpc
from apps.grpc_app.task_servicer import TaskServicer

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_opentelemetry():
    """OpenTelemetry 설정"""
    # Tracer Provider 설정
    trace.set_tracer_provider(TracerProvider())
    
    # Console Exporter 추가 (개발용)
    console_exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(console_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # gRPC 서버 instrumentation
    GrpcInstrumentorServer().instrument()

def serve():
    # OpenTelemetry 설정
    setup_opentelemetry()
    
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # gRPC 서버 설정
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    
    # Task 서비스 등록
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskServicer(), server)
    
    # 서버 시작
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"gRPC server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
