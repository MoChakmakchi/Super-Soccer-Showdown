# Define the Python version as a build argument
ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install build dependencies and pip in a separate layer to improve caching
FROM base AS builder

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip

# Copy only the requirements file to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# Create a minimal runtime image from the base image
FROM base AS runtime

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/ /usr/local/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container
COPY --chown=appuser:appuser . .

# Expose the port that the application listens on
EXPOSE 8000

# Add a health check to monitor the application status
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
