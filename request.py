import requests

# Define the FastAPI endpoint URL
url = "http://127.0.0.1:8000/compare-notes"

# Paths to the notes and transcript files
notes_file_path = "test_input/notes.txt"
transcript_file_path = "test_input/message.txt"

# Output file to save the enhanced notes
output_file_path = "test_output/enhanced_notes.txt"

# Prepare the files for the request
files = {
    "notes_file": open(notes_file_path, "rb"),
    "transcript_file": open(transcript_file_path, "rb"),
}

try:
    # Send the POST request to the FastAPI endpoint
    response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the enhanced notes from the response
        enhanced_notes = response.json().get("enhanced_notes", "")

        # Save the enhanced notes to a file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(enhanced_notes)

        print(f"Enhanced notes saved to {output_file_path}")
        print("Enhanced Notes:\n", enhanced_notes)
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")

finally:
    # Close the files
    for file in files.values():
        file.close()
