import streamlit as st

from meeting.transcription import transcribe_audio, get_realtime_insights
from meeting.meeting_save import generate_meeting_object, save_meeting_to_json
import os
import time
import queue
import cv2
import streamlit as st
import numpy as np
import tempfile



import pyaudio
import wave
import cv2
import threading
import json



is_recording = False
is_live_transcription = False
transcript_queue = queue.Queue()
stop_button_pressed=False

import cv2




import streamlit as st
import subprocess
import os

import os
import subprocess
import streamlit as st


import os
import subprocess
import webbrowser
import time

def run_main_py():
    # Define the path to your main.py file
    print("run_main_py")
    main_py_path = "video-meeting-zego/main.py"
    
    # Check if the file exists
    if not os.path.exists(main_py_path):
        print("The specified main.py file does not exist.")
        return
    
    try:
        # Use subprocess.Popen to run main.py in a non-blocking way
        process = subprocess.Popen(["python", main_py_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait a few seconds to ensure the server starts before opening the browser
        time.sleep(3)  # Adjust this delay based on how long main.py takes to start

        # Open localhost:5000 in the default browser
        webbrowser.open("http://localhost:5000")

        # Read the output line by line (so it doesn’t get stuck)
        print("### Output from main.py")
        for line in iter(process.stdout.readline, ''):
            print(line.strip())

        # Wait for the process to finish
        process.wait()

        # Check for errors
        stderr_output = process.stderr.read().strip()
        if stderr_output:
            print("### Error from main.py")
            print(stderr_output)

    except Exception as e:
        print(f"An error occurred: {e}")







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
    frame_placeholder = st.empty()
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
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB")
            audio_data = audio_stream.read(chunk)
            audio_frames.append(audio_data)
            transcription_frames.append(audio_data)
            if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed: 
                break

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
        
        cap.release()
        cv2.destroyAllWindows()

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
    if st.button("Start meeting"):
        
        start_recording_and_transcription(file_path_audio, file_path_video)
        
       

    if st.button("Stop meeting"):
        stop_recording_and_transcription()
        stop_button_pressed=True
         # This will stop the video feed
         # Wait for the video thread to finish


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

 

    st.subheader("Real-Time Insights:")
    insights_placeholder = st.empty()

    while True:  # Main loop for updating insights
        if not is_live_transcription and transcript_queue.empty():
            break  # Break out of the loop if not transcribing and queue is empty

        while not transcript_queue.empty():
            transcript = transcript_queue.get()
            print("Transcript received in main file:", transcript)

            if transcript:  # Ensure transcript is not None or empty
                if isinstance(transcript, dict):
                    # transcript = json.dumps(transcript, indent=2)  # Convert dict to a formatted string
                    st.write(transcript)

                st.session_state["live_insights"] = transcript 
        insights_placeholder.write(st.session_state["live_insights"])  # Update the placeholder
        time.sleep(3)  # Adjust update frequency as needed

if __name__ == "_main_":
    render_meeting_tab()