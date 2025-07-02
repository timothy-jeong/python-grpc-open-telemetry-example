import logging
from concurrent import futures

import grpc
from grpc_observability import OpenTelemetryServerInterceptor

from core.database import Base, engine
import task_pb2_grpc
from task_servicer import TaskServicer

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def serve():
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # gRPC 서버 설정
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[OpenTelemetryServerInterceptor()]
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
