import streamlit as st
import wave
import pyaudio
import os
import uuid
from datetime import datetime
import requests

# ChatGroq API keys
CHATGROQ_API_URL_TRANSCRIBE = "https://api.groq.com/openai/v1/audio/transcriptions"
CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your actual ChatGroq API key
import streamlit as st
import wave
import pyaudio
import os
import threading

# Global variable to control recording state
is_recording = False


# Function to record audio
def record_audio_continuously(file_path):
    global is_recording
    p = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    st.write("Recording started...")

    frames = []
    try:
        while is_recording:
            data = stream.read(chunk)
            frames.append(data)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        st.write("Recording completed.")

# Function to transcribe audio using ChatGroq
def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        st.error("Audio file not found!")
        return None

    try:
        with open(file_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {"model": "whisper-large-v3", "response_format": "json", "temperature": 0}
            headers = {"Authorization": f"Bearer {API_KEY}"}

            response = requests.post(CHATGROQ_API_URL_TRANSCRIBE, files=files, data=data, headers=headers)

        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            st.error(f"Transcription API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

# Function to generate meeting object using ChatGroq
import requests
import json
import streamlit as st
import os

# ChatGroq API Details
CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"  # Ensure this is the correct API endpoint
API_KEY = "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"  # Replace with your ChatGroq API key

# Function to generate meeting object using ChatGroq
def generate_meeting_object(transcript):
    prompt = (
        f"Given the following meeting transcript:\n\n{transcript}\n\n"
        "Create a structured JSON object in the format:\n"
        "{\n"
        "  \"meeting_id\": \"M001\",\n"
        "  \"title\": \"AI Team Weekly Sync\",\n"
        "  \"participants\": [\"Alice Johnson\", \"Bob Smith\", \"Charlie Brown\", \"Diana Lee\"],\n"
        "  \"date\": \"2025-01-20\",\n"
        "  \"duration\": \"1h 15m\",\n"
        "  \"agenda\": [\n"
        "    \"Review of last week's progress\",\n"
        "    \"Discussion on model accuracy improvements\",\n"
        "    \"Planning for upcoming project deadlines\"\n"
        "  ],\n"
        "  \"transcript\": [\n"
        "    {\n"
        "      \"timestamp\": \"00:05:23\",\n"
        "      \"speaker\": \"Alice Johnson\",\n"
        "      \"text\": \"Let's start by reviewing last week's tasks. Bob, can you give us a quick update?\"\n"
        "    },\n"
        "    {\n"
        "      \"timestamp\": \"00:10:45\",\n"
        "      \"speaker\": \"Bob Smith\",\n"
        "      \"text\": \"Sure, the model's accuracy improved by 5% after the latest training dataset update.\"\n"
        "    },\n"
        "    {\n"
        "      \"timestamp\": \"00:25:10\",\n"
        "      \"speaker\": \"Charlie Brown\",\n"
        "      \"text\": \"We need to focus on optimizing the hyperparameters for better efficiency.\"\n"
        "    }\n"
        "  ],\n"
        "  \"action_items\": [\n"
        "    \"Bob to provide a detailed report on model accuracy by Jan 25.\",\n"
        "    \"Charlie to investigate hyperparameter tuning options and present findings in the next meeting.\",\n"
        "    \"Diana to schedule a client review session for February.\"\n"
        "  ]\n"
        "}\n"
        "Respond only with the JSON object, no preamble or explanation."
    )

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",  # ChatGroq model to use
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }

        response = requests.post(CHATGROQ_API_URL_CHAT, json=payload, headers=headers)
        print(response.json());

        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", {})
        else:
            st.error(f"ChatGroq API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating meeting object: {e}")
        return None

# Function to start recording in a separate thread
def start_recording(file_path):
    global is_recording
    is_recording = True
    recording_thread = threading.Thread(target=record_audio_continuously, args=(file_path,))
    recording_thread.start()


# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False


# Function to save the meeting object into the JSON file
# def save_meeting_to_json(meeting_object):
#     # Read existing data from the file
#     if os.path.exists("data/meetings.json"):
#         with open("data/meetings.json", 'r', encoding='utf-8') as f:
#             meetings_data = json.load(f)
#     else:
#         meetings_data = []

#     # Add the new meeting object to the list
#     meetings_data.append(meeting_object)

#     # Write back to the file
#     with open("data/meetings.json", 'w', encoding='utf-8') as f:
#         json.dump(meetings_data, f, indent=4)


# Function to save the meeting object into the JSON file
def save_meeting_to_json(meeting_object):
    # Read existing data from the file
    if os.path.exists("data/meetings.json"):
        with open("data/meetings.json", 'r', encoding='utf-8') as f:
            meetings_data = json.load(f)
    else:
        meetings_data = []

    # Add the new meeting object to the list
    meetings_data.append(meeting_object)

    # Write back to the file
    with open("data/meetings.json", 'w', encoding='utf-8') as f:
        # Use json.dumps with indent for pretty printing
        f.write(json.dumps(meetings_data, indent=4))

# Streamlit UI logic
def render_meeting_tab():
    st.title("Meeting Recorder with ChatGroq")
    file_path = "meeting_audio.wav"

    # Start Recording button
    if st.button("Start Recording"):
        start_recording(file_path)

    # Stop Recording button
    if st.button("Stop Recording"):
        stop_recording()

    # Transcribe button
    if os.path.exists(file_path) and st.button("Transcribe Audio"):
        transcript = transcribe_audio(file_path)
        if transcript:
            st.subheader("Transcript:")
            st.write(transcript)

            # Generate meeting object
            meeting_object = generate_meeting_object(transcript)
            if meeting_object:
                st.subheader("Generated Meeting Object:")
                st.json(meeting_object)

                # Save the meeting object to the meetings.json file
                save_meeting_to_json(meeting_object)
                st.success("Meeting data has been saved to meetings.json.")

# Main entry point
if __name__ == "__main__":
    render_meeting_tab()