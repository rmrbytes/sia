FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt
COPY ./requirements.txt .

# Install dependencies
RUN pip install  --no-cache-dir --upgrade -r requirements.txt

# Copy python code 
COPY . .

# Run the script to download the model
CMD ["python", "download_model.py"]

