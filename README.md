# leedshack
To run this FastAPI backend:

### 1. Install Ollama.
Choose an appropriate version [here](https://ollama.com/download).
You should also pull a model you want to use:
`ollama pull deepseek-r1:1.5b`
(This will download the model to your machine)

### 2. Install required python libraries.
```pip install -r requirements.txt```

### 3. Run the backend.
In terminal run: ```uvicorn main:app --reload```

### 4. Test the endpoint.
You can test the endpoint by running the `request.py` script.
