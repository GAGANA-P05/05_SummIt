import pyaudio
import wave
import cv2
import threading
import time
import os
import queue
from meeting.transcription import transcribe_audio, get_realtime_insights
import streamlit as st
from meeting.meeting_main import record_audio_and_video,is_live_transcription,is_recording

# is_recording = False
# is_live_transcription = False
# transcript_queue = queue.Queue()



# def record_audio_and_video(file_path_audio, file_path_video):
#     global is_recording, is_live_transcription

#     # Initialize audio
#     p = pyaudio.PyAudio()
#     audio_format = pyaudio.paInt16
#     channels = 1
#     rate = 44100
#     chunk = 1024
#     audio_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

#     # Initialize video
#     cap = cv2.VideoCapture(0)  # 0 for default camera
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     frame_width = int(cap.get(3))
#     frame_height = int(cap.get(4))
#     video_writer = cv2.VideoWriter(file_path_video, fourcc, 20.0, (frame_width, frame_height))

#     st.write("Recording started...")

#     audio_frames = []
#     transcription_frames = []
#     start_time = time.time()

#     try:
#         while is_recording:
#             # Capture video frame
#             ret, frame = cap.read()
#             if ret:
#                 video_writer.write(frame)

#             # Capture audio data
#             audio_data = audio_stream.read(chunk)
#             audio_frames.append(audio_data)
#             transcription_frames.append(audio_data)

#             # Periodically send audio chunks for transcription
#             if time.time() - start_time >= 13:  # Every 3 seconds
#                 if is_live_transcription:
#                     with wave.open("temp_audio.wav", 'wb') as wf:
#                         wf.setnchannels(channels)
#                         wf.setsampwidth(p.get_sample_size(audio_format))
#                         wf.setframerate(rate)
#                         wf.writeframes(b''.join(transcription_frames))
                    
#                     transcript = transcribe_audio("temp_audio.wav")
#                     print("transcripteddata:",transcript)  
#                     data = get_realtime_insights(transcript)


#                     if transcript:
#                         print("Transcript received:", data)
#                         transcript_queue.put(data) 

#                 transcription_frames = []
#                 start_time = time.time()

#     finally:
#         # Stop and release resources
#         audio_stream.stop_stream()
#         audio_stream.close()
#         p.terminate()

#         cap.release()
#         video_writer.release()

#         # Save audio
#         with wave.open(file_path_audio, 'wb') as wf:
#             wf.setnchannels(channels)
#             wf.setsampwidth(p.get_sample_size(audio_format))
#             wf.setframerate(rate)
#             wf.writeframes(b''.join(audio_frames))

#         st.write("Recording completed.")




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
