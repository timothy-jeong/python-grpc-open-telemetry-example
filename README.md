# Python gRPC OpenTelemetry Example

This project demonstrates comprehensive monitoring system implementations for FastAPI and gRPC services using OpenTelemetry. It provides two different monitoring solutions to showcase various approaches to observability.

## 📋 Branch Overview

This repository consists of branches that demonstrate two different monitoring approaches:

### 🔗 Available Branches

## 📊 [Grafana Version](https://github.com/timothy-jeong/python-grpc-open-telemetry-example/tree/grafana-version)
> **Traditional Monitoring Stack**: Prometheus + Grafana

**Features:**
- **Prometheus**: Metrics collection and storage
- **Grafana**: Real-time dashboards and visualization
- **OpenTelemetry**: Distributed tracing and metrics collection
- **PostgreSQL**: Application data storage

**Key Components:**
- Prometheus metrics for FastAPI and gRPC services
- Pre-configured Grafana dashboards (FastAPI, gRPC)
- Full stack management with Docker Compose
- Real-time metrics monitoring and alerting

**Best suited for:**
- Teams preferring traditional monitoring stacks
- Organizations with existing Prometheus/Grafana infrastructure
- Use cases requiring detailed metrics customization

---

## 🔥 [Logfire Version](https://github.com/timothy-jeong/python-grpc-open-telemetry-example/tree/logfire-version)
> **Integrated Observability Platform**: Logfire

**Features:**
- **Logfire**: Integrated observability platform
- **Structured Logging**: Rich context request/response logging
- **Performance Monitoring**: Request duration and performance metrics
- **Error Tracking**: Comprehensive error logging and debugging

**Key Components:**
- FastAPI automatic instrumentation
- SQLAlchemy database query monitoring
- Custom gRPC service logging
- Unified logs, metrics, and tracing

**Best suited for:**
- Teams wanting modern integrated observability solutions
- Use cases where structured logging and performance analysis are critical
- Organizations preferring simple setup solutions

---

## 🏗️ Common Architecture

Both branches share the following common architecture:

### Service Components
- **FastAPI Application**: REST API service
- **gRPC Service**: High-performance RPC communication
- **Shared Core Module**: Database models and business logic
- **PostgreSQL**: Database storage

### Technology Stack
- **Python 3.12+**: Primary development language
- **OpenTelemetry**: Vendor-neutral observability
- **Docker & Docker Compose**: Container-based deployment
- **Protocol Buffers**: gRPC interface definition
- **SQLAlchemy**: ORM and database management

## 🚀 Quick Start

### 1. Choose a Branch
Select a branch based on your preferred monitoring solution:

```bash
# Grafana/Prometheus version
git checkout grafana-version

# Logfire version  
git checkout logfire-version
```

### 2. Follow Branch-specific README
Check the README.md file in your chosen branch for detailed installation and setup instructions.

## 📝 Project Goals

This project demonstrates:

1. **Modular Architecture**: Shared business logic between FastAPI and gRPC services
2. **Comprehensive Monitoring**: Two different approaches to observability implementation
3. **Container-based Deployment**: Full stack management with Docker Compose
4. **OpenTelemetry Standards Compliance**: Vendor-neutral observability implementation

## 🔗 References

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/languages/python/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Logfire Documentation](https://logfire.pydantic.dev/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## 📄 License

This project is distributed under the Apache License 2.0.

---

**🎯 Get started by clicking one of the branch links above to choose your preferred monitoring solution!**
