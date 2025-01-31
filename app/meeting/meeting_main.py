import streamlit as st
from recording import start_recording_and_transcription, stop_recording_and_transcription
from transcription import transcribe_audio, get_realtime_insights
from meeting_save import generate_meeting_object, save_meeting_to_json
import os
import time
import queue

# Global queue for real-time transcription updates
transcript_queue = queue.Queue()

def render_meeting_tab():
    st.title("Meeting Recorder with Video and Audio")

    # Initialize session state for live insights
    if "live_insights" not in st.session_state:
        st.session_state["live_insights"] = "No live insights yet."

    file_path_audio = "meeting_audio.wav"
    file_path_video = "meeting_video.avi"

    if st.button("Start Recording"):
        start_recording_and_transcription(file_path_audio, file_path_video)

    if st.button("Stop Recording"):
        stop_recording_and_transcription()

    if os.path.exists(file_path_audio) and os.path.exists(file_path_video):
        st.subheader("Download Recorded Files:")
        st.download_button("Download Audio", open(file_path_audio, "rb").read(), file_name="meeting_audio.wav", mime="audio/wav")
        st.download_button("Download Video", open(file_path_video, "rb").read(), file_name="meeting_video.avi", mime="video/x-msvideo")

        if st.button("Transcribe and Save Meeting"):
            transcript = transcribe_audio(file_path_audio)
            if transcript:
                st.subheader("Transcript:")
                st.write(transcript)

                meeting_object = generate_meeting_object(transcript)
                if meeting_object:
                    st.subheader("Generated Meeting Object:")
                    st.json(meeting_object)

                    save_meeting_to_json(meeting_object)
                    st.success("Meeting data has been saved to meetings.json.")

    # Real-time insights display
    st.subheader("Real-Time Insights:")
    insights_placeholder = st.empty()
    
    while True:
        if transcript_queue.empty():
            break
        while not transcript_queue.empty():
            transcript = transcript_queue.get()
            st.session_state["live_insights"] += transcript + "\n"

        insights_placeholder.write(st.session_state["live_insights"])
        time.sleep(3)

if __name__ == "__main__":
    render_meeting_tab()
