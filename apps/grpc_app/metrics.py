from prometheus_client import Counter, Histogram
# Prometheus metrics definitions

# gRPC request counter by method and status
grpc_request_counter = Counter(
    'grpc_request_total',
    'Total number of gRPC requests',
    ['method', 'status']
)

# gRPC request latency histogram
grpc_request_latency = Histogram(
    'grpc_request_duration_seconds',
    'gRPC request latency in seconds',
    ['method']
) 