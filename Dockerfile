# Use a minimal base image
FROM python:3.10-alpine

# Install system dependencies for Python
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
