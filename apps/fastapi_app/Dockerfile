# Builder stage
FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app/

COPY . .

RUN uv sync --all-packages --no-dev


# Runtime stage
FROM python:3.12


# Create a non-root user
RUN groupadd -r app && useradd -r -g app app

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Set virtual environment path
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER app

EXPOSE 8000 

CMD uvicorn --host=0.0.0.0 main:app
