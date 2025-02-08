from fastapi import FastAPI, File, UploadFile, HTTPException
import ollama

app = FastAPI()


@app.post("/compare-notes")
async def compare_notes(
    notes_file: UploadFile = File(...), transcript_file: UploadFile = File(...)
):
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
