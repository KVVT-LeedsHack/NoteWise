from ollama import chat
from ollama import ChatResponse

transcript = open("message.txt", "r").read()
notes = open("notes.txt", "r").read()

stream = chat(
    model="deepseek-r1:1.5b",
    messages=[
        {
            "role": "user",
            "content": "Here are the notes:\n {}\n\n Here is the transcript: \n {} \n\n Compare the notes to the lecture transcript. Identify key missing points from the notes and fill in the gaps. Do not remove any information from the notes unless it is wrong.".format(
                notes, transcript
            ),
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
