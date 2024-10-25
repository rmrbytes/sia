# Use a lightweight base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first for better layer caching
COPY requirements.txt .

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8002

# Start the uvicorn server with the specified number of workers
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8002 --workers ${API_NO_WORKERS:-1}"]
