import pyaudio
import wave
import cv2
import threading
import time
import os
import queue
from transcription import transcribe_audio, get_realtime_insights

is_recording = False
is_live_transcription = False
transcript_queue = queue.Queue()

def record_audio_and_video(file_path_audio, file_path_video):
    global is_recording, is_live_transcription

    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    audio_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(file_path_video, fourcc, 20.0, (640, 480))

    audio_frames = []
    transcription_frames = []
    start_time = time.time()

    try:
        while is_recording:
            ret, frame = cap.read()
            if ret:
                video_writer.write(frame)

            audio_data = audio_stream.read(chunk)
            audio_frames.append(audio_data)
            transcription_frames.append(audio_data)

            if time.time() - start_time >= 3 and is_live_transcription:
                with wave.open("temp_audio.wav", 'wb') as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(p.get_sample_size(audio_format))
                    wf.setframerate(rate)
                    wf.writeframes(b''.join(transcription_frames))

                transcript = transcribe_audio("temp_audio.wav")
                data = get_realtime_insights(transcript)

                if transcript:
                    transcript_queue.put(data)

                transcription_frames = []
                start_time = time.time()

    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        cap.release()
        video_writer.release()

        with wave.open(file_path_audio, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(audio_frames))

def start_recording_and_transcription(file_path_audio, file_path_video):
    global is_recording, is_live_transcription
    is_recording = True
    is_live_transcription = True
    threading.Thread(target=record_audio_and_video, args=(file_path_audio, file_path_video)).start()

def stop_recording_and_transcription():
    global is_recording, is_live_transcription
    is_recording = False
    is_live_transcription = False
