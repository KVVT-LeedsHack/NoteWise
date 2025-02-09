from fastapi import FastAPI, File, UploadFile, HTTPException
import ollama
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables (for API key)
load_dotenv()

# Configure Gemini with your API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
client = genai.Client(api_key=gemini_api_key)

app = FastAPI()

def process_files(notes: UploadFile, transcript: UploadFile, model_type: str):
    """
    Helper function to process the files, generate prompts, and enhance the notes.
    """
    # Read and decode the uploaded files
    notes_content = notes.file.read().decode("utf-8")
    transcript_content = transcript.file.read().decode("utf-8")
    
    enhanced_notes = ""
    chunk_size = 32000  # Adjust chunk size based on model's token limit

    # Process the input in chunks (if necessary)
    for i in range(0, max(len(notes_content), len(transcript_content)), chunk_size):
        notes_chunk = notes_content[i: i + chunk_size]
        transcript_chunk = transcript_content[i: i + chunk_size]

        # Prepare the prompt for comparison
        prompt = f"""
        Imagine you are a study assistant. You are provided with a chunk here of a student's self-written lecture notes (Notes Chunk) and a chunk of the full transcript from their lecture (Transcript Chunk). Compare the following notes chunk with the transcript chunk and identify topics, concepts that the student has missed in their written notes. Enhance the notes by adding the relevant missing information. Provide the enhanced note chunk directly.:
        
        Notes Chunk:
        {notes_chunk}

        Transcript Chunk:
        {transcript_chunk}

        Provide the enhanced notes for this chunk.
        Provide answer directly.
        """

        try:
            # Make API request based on model type
            if model_type == "ollama":
                response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
                enhanced_notes += response["response"] + "\n"
            elif model_type == "gemini":
                response = client.models.generate_content(
                    model="gemini-2.0-flash",  # Update the model name as needed
                    contents=prompt
                )
                enhanced_notes += response.text + "\n"
            else:
                raise ValueError("Invalid model type specified.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return enhanced_notes

@app.post("/compare-notes")
async def compare_notes(
    notes_file: UploadFile = File(...), transcript_file: UploadFile = File(...),
):
    """
    Compare notes using the Ollama model.
    """
    enhanced_notes = process_files(notes_file, transcript_file, model_type="ollama")
    return {"enhanced_notes": enhanced_notes}

@app.post("/compare-notes-gemini")
async def compare_notes_gemini(
    notes_file: UploadFile = File(...), transcript_file: UploadFile = File(...),
):
    """
    Compare notes using the Gemini model.
    """
    enhanced_notes = process_files(notes_file, transcript_file, model_type="gemini")
    return {"enhanced_notes": enhanced_notes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
