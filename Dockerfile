FROM python:3.12-slim

WORKDIR /app

# Copy source code (service has no external dependencies)
COPY src/service /app

# Expose default port
EXPOSE 5000

# Run the service
CMD ["python", "main.py"]
