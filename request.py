import requests
import os
import time

# Define the FastAPI endpoint URL
url = "http://127.0.0.1:8000/compare-notes"
gemini_url = "http://127.0.0.1:8000/compare-notes-gemini"

# Paths to the notes and transcript files
notes_file_path = "test_input/notes.txt"
transcript_file_path = "test_input/message.txt"

# Output file to save the enhanced notes
# check if the test_output folder exists, if not create it
if not os.path.exists("test_output"):
    os.makedirs("test_output")
    
output_file_path = "test_output/enhanced_notes.txt"
gemini_output_file_path = "test_output/gemini_enhanced_notes.txt"


# Prepare the files for the request
files = {
    "notes_file": open(notes_file_path, "rb"),
    "transcript_file": open(transcript_file_path, "rb"),
}

try:
    # Time the time taken for DeepSeek to enhance the notes
    start_time  = time.time()   
    
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
        
    # Calculate the time taken for DeepSeek to enhance the notes
    end_time = time.time()  
    print("Time taken for DeepSeek to enhance the notes: ", end_time - start_time)
    
    # Time the time taken for Gemini to enhance the notes   
    g_start_time  = time.time()
        
    # Send the POST request to the FastAPI endpoint
    gemini_response = requests.post(gemini_url, files=files)

    # Check if the request was successful
    if gemini_response.status_code == 200:
        # Extract the enhanced notes from the response
        gemini_enhanced_notes = gemini_response.json().get("enhanced_notes", "")

        # Save the enhanced notes to a file
        with open(gemini_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(gemini_enhanced_notes)

        print(f"Enhanced notes saved to {gemini_output_file_path}")
        print("Enhanced Notes:\n", gemini_enhanced_notes)
    else:
        # Handle errors
        print(f"Error: {gemini_response.status_code} - {gemini_response.text}")
        
    # Calculate the time taken for Gemini to enhance the notes
    g_end_time = time.time()  
    print("Time taken for Gemini to enhance the notes: ", g_end_time - g_start_time)

finally:
    # Close the files
    for file in files.values():
        file.close()
