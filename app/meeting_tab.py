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


import streamlit as st
import wave
import pyaudio
import cv2
import threading
import os

# Global variable for controlling recording
is_recording = False

def record_audio_and_video(file_path_audio, file_path_video):
    global is_recording

    # Initialize audio
    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    audio_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    # Initialize video
    cap = cv2.VideoCapture(0)  # 0 for default camera
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    video_writer = cv2.VideoWriter(file_path_video, fourcc, 20.0, (frame_width, frame_height))

    st.write("Recording started...")

    audio_frames = []

    try:
        while is_recording:
            # Capture video frame
            ret, frame = cap.read()
            if ret:
                video_writer.write(frame)

            # Capture audio data
            audio_data = audio_stream.read(chunk)
            audio_frames.append(audio_data)

    finally:
        # Stop and release resources
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()

        cap.release()
        video_writer.release()

        # Save audio
        with wave.open(file_path_audio, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(audio_frames))

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
def start_recording(file_path_audio, file_path_video):
    global is_recording
    is_recording = True
    threading.Thread(target=record_audio_and_video, args=(file_path_audio, file_path_video)).start()

def stop_recording():
    global is_recording
    is_recording = False



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

def render_meeting_tab():
    st.title("Meeting Recorder with Video and Audio")

    # File paths
    file_path_audio = "meeting_audio.wav"
    file_path_video = "meeting_video.avi"

    # Start Recording button
    if st.button("Start Recording"):
        start_recording(file_path_audio, file_path_video)

    # Stop Recording button
    if st.button("Stop Recording"):
        stop_recording()

    # Provide download buttons after recording
    if os.path.exists(file_path_audio) and os.path.exists(file_path_video):
        st.subheader("Download Recorded Files:")
        st.download_button(
            label="Download Audio",
            data=open(file_path_audio, "rb").read(),
            file_name="meeting_audio.wav",
            mime="audio/wav"
        )
        st.download_button(
            label="Download Video",
            data=open(file_path_video, "rb").read(),
            file_name="meeting_video.avi",
            mime="video/x-msvideo"
        )

        # Transcribe audio
        if st.button("Transcribe and Save Meeting"):
            transcript = transcribe_audio(file_path_audio)
            if transcript:
                st.subheader("Transcript:")
                st.write(transcript)

                # Generate and save meeting object
                meeting_object = generate_meeting_object(transcript)
                if meeting_object:
                    st.subheader("Generated Meeting Object:")
                    st.json(meeting_object)

                    save_meeting_to_json(meeting_object)
                    st.success("Meeting data has been saved to meetings.json.")


# Main entry point
if __name__ == "__main__":
    render_meeting_tab()






import streamlit as st
import wave
import pyaudio
import cv2
import threading
import os
import requests
import time

# ChatGroq API Details
CHATGROQ_API_URL_TRANSCRIBE = "https://api.groq.com/openai/v1/audio/transcriptions"
CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "your_groq_api_key"  # Replace with your actual ChatGroq API key

# Global variable for controlling real-time transcription
is_live_transcription = False

def record_audio_chunk(file_path_audio):
    """Records a short audio chunk and saves it."""
    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    
    audio_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []
    
    for _ in range(0, int(rate / chunk * 3)):  # Record for 3 seconds
        data = audio_stream.read(chunk)
        frames.append(data)
    
    audio_stream.stop_stream()
    audio_stream.close()
    p.terminate()
    
    with wave.open(file_path_audio, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def transcribe_audio(file_path):
    """Transcribes the recorded audio chunk."""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"model": "whisper-large-v3", "response_format": "json", "temperature": 0}
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(CHATGROQ_API_URL_TRANSCRIBE, files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("text", "")
    return None

def get_real_time_insights(transcript):
    """Fetches real-time insights based on the transcript."""
    prompt = f"Generate real-time insights and suggestions based on the following conversation:\n{transcript}\n\nProvide actionable insights."
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    
    response = requests.post(CHATGROQ_API_URL_CHAT, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    return "No insights available."

def start_live_transcription():
    """Continuously records, transcribes, and fetches insights every 3 seconds."""
    global is_live_transcription
    is_live_transcription = True
    
    while is_live_transcription:
        file_path_audio = "live_audio.wav"
        record_audio_chunk(file_path_audio)
        transcript = transcribe_audio(file_path_audio)
        
        if transcript:
            insights = get_real_time_insights(transcript)
            st.session_state["live_insights"] = insights
        time.sleep(3)

def stop_live_transcription():
    """Stops live transcription."""
    global is_live_transcription
    is_live_transcription = False

def render_live_transcription_tab():
    st.title("Live Meeting Insights")
    
    if "live_insights" not in st.session_state:
        st.session_state["live_insights"] = ""
    
    if st.button("Start Live Insights"):
        threading.Thread(target=start_live_transcription, daemon=True).start()
    
    if st.button("Stop Live Insights"):
        stop_live_transcription()
    
    st.subheader("Real-Time Insights:")
    st.write(st.session_state["live_insights"])
    
if __name__ == "__main__":
    render_live_transcription_tab()