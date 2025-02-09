#!/bin/bash
# Pull the Ollama model
ollama pull deepseek-r1:1.5b

# Start the FastAPI app
uvicorn main:app --host 0.0.0.0 --port 80