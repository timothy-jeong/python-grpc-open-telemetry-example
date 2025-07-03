# Python gRPC OpenTelemetry Example

> **Note**: This is the `logfire-version` branch, which implements monitoring using Logfire observability platform.

A comprehensive monitoring system implementation example for FastAPI and gRPC services using OpenTelemetry. Provides real-time monitoring through Logfire's integrated observability platform with structured logging, metrics, and distributed tracing.

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
│       ├── test_client.py        # gRPC test client
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
├── docker-compose.yaml           # Full stack orchestration
├── Dockerfile.fastapi
├── Dockerfile.grpc
├── env.example                   # Environment variables template
├── pyproject.toml
└── uv.lock
```

## 🚀 Key Features

### 📊 Monitoring Stack
- **OpenTelemetry**: Distributed tracing and metrics collection
- **Logfire**: Integrated observability platform with structured logging
- **PostgreSQL**: Application data storage
- **Docker Compose**: Service orchestration

### 🔧 Service Architecture
- **FastAPI Application**: REST API service
- **gRPC Service**: High-performance RPC communication
- **Shared Core Module**: Database models and business logic

## 📈 Observability with Logfire

### Logfire Integration
This project uses [Logfire](https://logfire.pydantic.dev/) as the primary observability platform, providing:
- **Structured Logging**: Detailed request/response logging with context
- **Performance Monitoring**: Request duration and performance metrics
- **Error Tracking**: Comprehensive error logging and debugging
- **Distributed Tracing**: Full request flow across services

#### Server-side Instrumentation
```python
import logfire

# Configure Logfire
logfire.configure()

# Instrument FastAPI
logfire.instrument_fastapi(app)

# Instrument SQLAlchemy
logfire.instrument_sqlalchemy(engine=engine)
```

#### gRPC Service Logging
```python
import logfire

# Log gRPC operations
logfire.info("Processing gRPC request", method=method, request_data=request_data)
logfire.info("gRPC request completed", method=method, duration=duration, status="success")
```

### Monitoring Features
- **Request Tracking**: All HTTP and gRPC requests with timing
- **Database Operations**: SQL query monitoring and performance
- **Error Logging**: Detailed error context and stack traces
- **Performance Metrics**: Response times and throughput analysis

## 🛠️ Installation and Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)
- uv (Python package manager)
- Logfire account and **write token**

### 1. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env file and add your Logfire write token
# LOGFIRE_TOKEN=your_logfire_write_token_here
```

> **Important**: You need a Logfire **write token** (not a read token) to send logs and metrics to Logfire. You can get this from your Logfire project settings.

### 2. Run the Full Stack
```bash
# Start all services
docker compose up -d --build

# Check service status
docker compose ps
```

### 3. Access Services
- **Logfire Dashboard**: https://logfire.pydantic.dev (your project dashboard)
- **FastAPI Documentation**: http://localhost:8000/docs
- **gRPC Service**: localhost:50051
- **PostgreSQL**: localhost:5432

### 4. Run Tests
```bash
# gRPC client test
uv run python apps/grpc_app/test_client.py

# FastAPI test
curl http://localhost:8000/tasks
```

### 5. Generate Monitoring Data
```bash
# Generate multiple test requests to see logging in action
for i in {1..10}; do
  echo "Running test $i..."
  uv run python apps/grpc_app/test_client.py
  sleep 1
done

# Test FastAPI endpoints
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Test Description"}'

curl http://localhost:8000/tasks
```

## 📊 Logfire Dashboard Features

### Real-time Monitoring
- **Request Logs**: All HTTP and gRPC requests with detailed context
- **Performance Metrics**: Response times and request volumes
- **Error Tracking**: Failed requests with full error context
- **Database Queries**: SQL execution times and query analysis

### Key Metrics Tracked
- **FastAPI Endpoints**: Request duration, status codes, endpoint usage
- **gRPC Methods**: Method calls, response times, success/failure rates
- **Database Operations**: Query performance, connection usage
- **System Health**: Overall service performance and error rates

### Viewing Logs and Metrics
1. Open your Logfire dashboard at https://logfire.pydantic.dev
2. Navigate to your project
3. View real-time logs and metrics
4. Use filters to focus on specific services or time ranges
5. Analyze performance trends and identify issues

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
docker compose up -d postgres

# Set up environment variables
cp env.example .env
# Edit .env and add your LOGFIRE_TOKEN (write token)

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

# Create test data
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Development Task", "description": "Testing Logfire integration"}'

# Monitor logs in real-time via Logfire dashboard
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

### 2. Comprehensive Observability
- Structured logging with rich context
- Automatic request/response tracking
- Performance monitoring and analysis
- Error tracking and debugging

### 3. Container-based Deployment
- Full stack management with Docker Compose
- Development/production environment consistency
- Secure environment variable management

### 4. OpenTelemetry Standards Compliance
- Vendor-neutral observability implementation
- Standard metrics and trace formats
- Seamless integration with Logfire platform

## 🔧 Configuration

### Environment Variables
```bash
# Required - Logfire write token for sending logs and metrics
LOGFIRE_TOKEN=your_logfire_write_token_here

# Database (automatically configured in Docker)
DATABASE_URL=postgresql://user:password@localhost:5432/taskdb
```

### Logfire Configuration
The project automatically configures Logfire for:
- FastAPI request/response logging
- SQLAlchemy database query monitoring
- Custom gRPC service logging
- Error tracking and performance monitoring

## 📄 License

This project is distributed under the Apache License 2.0.

## 🔗 References

- [Logfire Documentation](https://logfire.pydantic.dev/)
- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/languages/python/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
