# Python gRPC OpenTelemetry Example

> **Note**: This is the `grafana-version` branch, which implements monitoring using Grafana dashboards.

A comprehensive monitoring system implementation example for FastAPI and gRPC services using OpenTelemetry. Provides real-time monitoring through Prometheus metrics collection and Grafana dashboards.

## 🏗️ Project Structure

```
python-grpc-open-telemetry-example/
├── apps/
│   ├── fastapi_app/              # FastAPI application
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── grpc_app/                 # gRPC service
│       ├── main.py               # gRPC server main
│       ├── task_servicer.py      # TaskService implementation
│       ├── task_pb2.py           # Generated protobuf files
│       ├── task_pb2_grpc.py      # Generated gRPC files
│       ├── metrics.py            # Prometheus metrics definitions
│       ├── test_client.py        # gRPC test client
│       ├── open_telemetry_exporter.py  # OpenTelemetry configuration
│       ├── pyproject.toml
│       └── README.md
├── core/                         # Shared business logic
│   ├── src/core/
│   │   ├── __init__.py
│   │   ├── database.py           # Database connection
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   └── services.py           # Business logic
│   ├── pyproject.toml
│   └── README.md
├── proto/
│   └── task.proto                # Protocol Buffers definition
├── grafana/
│   ├── config.monitoring
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboard.yml
│       │   ├── fastapi-dashboard.json
│       │   └── grpc-dashboard.json
│       └── datasources/
│           └── datasource.yml
├── prometheus/
│   └── prometheus.yml            # Prometheus configuration
├── docker-compose.yaml           # Full stack orchestration
├── Dockerfile.fastapi
├── Dockerfile.grpc
├── pyproject.toml
└── uv.lock
```

## 🚀 Key Features

### 📊 Monitoring Stack
- **OpenTelemetry**: Distributed tracing and metrics collection
- **Prometheus**: Metrics storage and querying
- **Grafana**: Real-time dashboards and visualization
- **PostgreSQL**: Application data storage

### 🔧 Service Architecture
- **FastAPI Application**: REST API service
- **gRPC Service**: High-performance RPC communication
- **Shared Core Module**: Database models and business logic

## 📈 Metrics and Tracing

### gRPC Metrics
- `grpc_request_total`: Total number of requests (by method and status)
- `grpc_request_duration_seconds`: Request response time histogram

### OpenTelemetry Implementation
This project uses [OpenTelemetry gRPC Instrumentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/grpc/grpc.html) to implement automatic instrumentation for gRPC services.

#### Server-side Instrumentation
```python
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()
```

#### Client-side Instrumentation
```python
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

grpc_client_instrumentor = GrpcInstrumentorClient()
grpc_client_instrumentor.instrument()
```

## 🛠️ Installation and Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)
- uv (Python package manager)

### 1. Run the Full Stack
```bash
# Start all services
docker compose up -d --build

# Check service status
docker compose ps
```

### 2. Access Services
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **FastAPI Documentation**: http://localhost:8000/docs
- **gRPC Service**: localhost:50051
- **PostgreSQL**: localhost:5432

### 3. Run Tests
```bash
# gRPC client test
uv run python apps/grpc_app/test_client.py

# FastAPI test
curl http://localhost:8000/tasks
```

### 4. Verify Metrics Collection
```bash
# Check Prometheus metrics endpoint
curl http://localhost:50052/metrics | grep grpc

# Query Prometheus API
curl "http://localhost:9090/api/v1/query?query=grpc_request_total"

# Generate more metrics with multiple test runs
for i in {1..5}; do
  echo "Running test $i..."
  uv run python apps/grpc_app/test_client.py
  sleep 1
done
```

## 📊 Grafana Dashboards

### FastAPI Dashboard
- HTTP request metrics
- Response time distribution
- Error rate tracking

### gRPC Dashboard
- **Request Rate**: Requests per second
- **Request Duration (p95)**: 95th percentile response time
- **Error Rate**: Error occurrence rate
- **Active Requests by Method**: Request statistics by method

### Viewing Dashboards
1. Open Grafana at http://localhost:3000
2. Login with `admin`/`pass@123`
3. Navigate to **Dashboards** → **Services**
4. Select either **FastAPI Dashboard** or **gRPC Service Dashboard**
5. Adjust time range to **Last 15 minutes** for recent data
6. Run test clients to generate metrics and see real-time updates

## 🔍 Protocol Buffers

gRPC interface for Task service:

```protobuf
service TaskService {
  rpc CreateTask (CreateTaskRequest) returns (TaskResponse);
  rpc ListTasks (ListTasksRequest) returns (ListTasksResponse);
  rpc GetTask (GetTaskRequest) returns (TaskResponse);
  rpc UpdateTask (UpdateTaskRequest) returns (TaskResponse);
  rpc DeleteTask (DeleteTaskRequest) returns (DeleteTaskResponse);
}
```

## 🧪 Development Environment

### Local Development Setup
```bash
# Install dependencies
uv sync --all-packages

# Run development servers (PostgreSQL via Docker)
docker compose up -d postgres prometheus grafana

# FastAPI development server
cd apps/fastapi_app && uv run uvicorn main:app --reload

# gRPC server
cd apps/grpc_app && uv run python main.py
```

### Testing and Monitoring
```bash
# Test gRPC service
uv run python apps/grpc_app/test_client.py

# Test FastAPI service
curl http://localhost:8000/tasks

# Monitor metrics in real-time
watch -n 2 'curl -s http://localhost:50052/metrics | grep grpc_request_total'

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets
```

### Code Generation
```bash
# Install dependencies
uv sync --all-packages

# Compile Protocol Buffers
uv run python -m grpc_tools.protoc \
    --proto_path=proto \
    --python_out=apps/grpc_app \
    --grpc_python_out=apps/grpc_app \
    proto/task.proto
```

## 📝 Key Implementation Features

### 1. Modular Architecture
- Separated business logic through shared core module
- Code reuse between FastAPI and gRPC services

### 2. Comprehensive Monitoring
- Automatic metrics collection
- Distributed tracing
- Real-time dashboards

### 3. Container-based Deployment
- Full stack management with Docker Compose
- Development/production environment consistency

### 4. OpenTelemetry Standards Compliance
- Vendor-neutral observability implementation
- Standard metrics and trace formats

## 📄 License

This project is distributed under the Apache License 2.0.

## 🔗 References

- [OpenTelemetry gRPC Instrumentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/grpc/grpc.html)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Grafana Documentation](https://grafana.com/docs/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
