# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Copy the current directory contents into the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Install Ollama (example for Linux)
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# Run the FastAPI app with Uvicorn
CMD ["./start.sh"]