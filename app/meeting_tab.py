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









import streamlit as st
import wave
import pyaudio
import os
import threading
import cv2
import time
import requests
import json

# Global variables to control recording and transcription state
is_recording = False
is_live_transcription = False

import pyaudio
import wave
import cv2
import threading
import time
import os
import streamlit as st
import queue

# Global variables
is_recording = False
is_live_transcription = False
transcript_queue = queue.Queue()  # Queue to hold transcript data

def get_realtime_insights(transcript_chunk):
    prompt = (
        f"Given the following meeting transcript chunk:\n\n{transcript_chunk}\n\n"
        "Provide real-time insights and suggestions for the conversation.  "
        "Focus on identifying key discussion points, potential issues, "
        "and actionable suggestions for improvement.  "
        "Respond in a concise and structured format, like this:\n\n"
        "```json\n"
        "{\n"
        "  \"key_discussion_points\": [\n"
        "    \"Mentioned the need for better client communication.\",\n"
        "    \"Discussed the Q3 budget and potential cost overruns.\",\n"
        "    \"Brainstormed new marketing strategies.\"\n"
        "  ],\n"
        "  \"potential_issues\": [\n"
        "    \"Client communication has been inconsistent and needs improvement.\",\n"
        "    \"Current spending trends indicate a possible budget deficit.\"\n"
        "  ],\n"
        "  \"suggestions\": [\n"
        "    \"Implement a weekly client update email.\",\n"
        "    \"Review the budget line items and identify areas for cost reduction.\",\n"
        "    \"Schedule a follow-up meeting to further discuss the marketing strategies.\"\n"
        "  ]\n"
        "}\n"
        "```\n"
        "Respond *only* with the JSON object. No preamble or explanation."
    )

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",  # Or another suitable model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,  # Keep temperature low for factual responses
        }

        response = requests.post(CHATGROQ_API_URL_CHAT, json=payload, headers=headers)

        if response.status_code == 200:
            try:  # Attempt to parse JSON response
                return json.loads(response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}"))
            except json.JSONDecodeError:
                st.error(f"Invalid JSON response from ChatGroq: {response.text}")
                return None
        else:
            st.error(f"ChatGroq API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting real-time insights: {e}")
        return None


def record_audio_and_video(file_path_audio, file_path_video):
    global is_recording, is_live_transcription

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
    transcription_frames = []
    start_time = time.time()

    try:
        while is_recording:
            # Capture video frame
            ret, frame = cap.read()
            if ret:
                video_writer.write(frame)

            # Capture audio data
            audio_data = audio_stream.read(chunk)
            audio_frames.append(audio_data)
            transcription_frames.append(audio_data)

            # Periodically send audio chunks for transcription
            if time.time() - start_time >= 13:  # Every 3 seconds
                if is_live_transcription:
                    with wave.open("temp_audio.wav", 'wb') as wf:
                        wf.setnchannels(channels)
                        wf.setsampwidth(p.get_sample_size(audio_format))
                        wf.setframerate(rate)
                        wf.writeframes(b''.join(transcription_frames))
                    
                    transcript = transcribe_audio("temp_audio.wav")
                    print("transcripteddata:",transcript)  
                    data = get_realtime_insights(transcript)


                    if transcript:
                        print("Transcript received:", data)
                        transcript_queue.put(data) 

                transcription_frames = []
                start_time = time.time()

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

def start_live_transcription():
    global is_live_transcription
    is_live_transcription = True

def stop_live_transcription():
    global is_live_transcription
    is_live_transcription = False

def start_recording_and_transcription(file_path_audio, file_path_video):
    global is_recording
    is_recording = True
    threading.Thread(target=record_audio_and_video, args=(file_path_audio, file_path_video)).start()
    start_live_transcription()

def stop_recording_and_transcription():
    global is_recording
    is_recording = False
    stop_live_transcription()

def render_meeting_tab():
    st.title("Meeting Recorder with Video and Audio")
    # Initialize session state for live insights
    if "live_insights" not in st.session_state:
        st.session_state["live_insights"] = "No live insights yet."

    # File paths for recording
    file_path_audio = "meeting_audio.wav"
    file_path_video = "meeting_video.avi"

    # Start and stop recording buttons
    if st.button("Start Recording"):
        start_recording_and_transcription(file_path_audio, file_path_video)

    if st.button("Stop Recording"):
        stop_recording_and_transcription()

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

        # Transcribe and save the meeting
        if st.button("Transcribe and Save Meeting"):
            transcript = transcribe_audio(file_path_audio)
            if transcript:
                st.subheader("Transcript:")
                st.write(transcript)

                # Generate and save meeting object (similar to earlier)
                meeting_object = generate_meeting_object(transcript)
                if meeting_object:
                    st.subheader("Generated Meeting Object:")
                    st.json(meeting_object)

                    save_meeting_to_json(meeting_object)
                    st.success("Meeting data has been saved to meetings.json.")

    # Real-time insights display
    st.subheader("Real-Time Insights:")
    insights_placeholder = st.empty()
    while True:  # Main loop for updating insights
        if not is_live_transcription and transcript_queue.empty():
            break # Break out of the loop if not transcribing and queue is empty

        while not transcript_queue.empty():
            transcript = transcript_queue.get()
            st.session_state["live_insights"] += transcript + "\n"

        insights_placeholder.write(st.session_state["live_insights"])  # Update the placeholder
        time.sleep(3)  # Adjust update frequency as needed

# Main entry point
if __name__ == "__main__":
    render_meeting_tab()