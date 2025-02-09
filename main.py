from fastapi import FastAPI, File, UploadFile, HTTPException
import ollama
import re
from pydantic import BaseModel

app = FastAPI(
    title="Lecture Notes Enhancer API",
    description="An API to enhance lecture notes by comparing them with a transcript using a locally running LLM.",
    version="1.0.0",
)


class NotesRequest(BaseModel):
    notes: str
    transcript: str


class EnhancedNotesResponse(BaseModel):
    enhanced_notes: str


@app.post(
    "/compare/deepseek",
    response_model=EnhancedNotesResponse,
    summary="Compare Notes and Transcript",
    description="Compare lecture notes with a transcript and fill in gaps using an LLM.",
)
async def compare_notes(
    notes_file: UploadFile = File(...), transcript_file: UploadFile = File(...)
):
    """
    Compare lecture notes with a transcript and generate enhanced notes.

    - **notes_file**: Upload a text file containing the lecture notes.
    - **transcript_file**: Upload a text file containing the lecture transcript.
    """
    # Read the uploaded files
    notes = await notes_file.read()
    transcript = await transcript_file.read()

    # Decode bytes to string (assuming the files are text-based)
    notes = notes.decode("utf-8")
    transcript = transcript.decode("utf-8")

    # Process the input in chunks (if necessary)
    enhanced_notes = ""
    chunk_size = 32000  # Adjust based on model's token limit
    for i in range(0, max(len(notes), len(transcript)), chunk_size):
        notes_chunk = notes[i : i + chunk_size]
        transcript_chunk = transcript[i : i + chunk_size]

        prompt = f"""
        Compare the following notes chunk with the corresponding transcript chunk and fill in any gaps:
        
        Notes Chunk:
        {notes_chunk}

        Transcript Chunk:
        {transcript_chunk}

        Provide the enhanced notes for this chunk.
        Provide answer directly.
        """

        try:
            response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
            enhanced_notes += response["response"] + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"enhanced_notes": enhanced_notes}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
