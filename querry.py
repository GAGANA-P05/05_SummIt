import os
import json
import datetime
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.2-90b-text-preview")

# Class for handling the dataset
class MeetingDataHandler:
    def __init__(self, file_path="meeting_data.json"):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def add_meeting(self, date, time, conversation, topic, attendees, conclusion):
        meeting_entry = {
            "date": date,
            "time": time,
            "conversation": conversation,
            "topic": topic,
            "attendees": attendees,
            "conclusion": conclusion
        }
        self.data.append(meeting_entry)
        self.save_data()

# Function to query and display meeting data
def query_meeting_data(query, data_handler):
    relevant_entries = []
    for entry in data_handler.data:
        if query.lower() in entry["conversation"].lower() or query.lower() in entry["topic"].lower():
            relevant_entries.append(entry)
    return relevant_entries

# Function to process audio/video transcription via Groq
def process_audio_transcription(audio_file):
    with open(audio_file, "rb") as f:
        transcription = llm.transcribe_audio(f.read())
    return transcription

# Streamlit interface
st.title("AI-Powered Meeting and Query Tool")
data_handler = MeetingDataHandler()

# Tabbed interface
query_tab, meeting_tab = st.tabs(["Query", "Meeting"])

# Query tab
with query_tab:
    st.header("Query Meeting Data")
    user_query = st.text_input("Enter your query")
    if st.button("Search"):
        results = query_meeting_data(user_query, data_handler)
        if results:
            st.json(results)
        else:
            st.write("No relevant data found.")

# Meeting tab
with meeting_tab:
    st.header("Record a Meeting")

    # Input fields for meeting details
    topic = st.text_input("Meeting Topic")
    attendees = st.text_input("Attendees (comma-separated)")
    uploaded_audio = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

    if st.button("Process Meeting"):
        if uploaded_audio and topic and attendees:
            # Transcribe audio
            transcription = process_audio_transcription(uploaded_audio)

            # Generate summary via LLM
            summary_prompt = f"Summarize the following meeting transcription:\n\n{transcription}"
            summary_response = llm.invoke(summary_prompt)
            summary = summary_response.content

            # Store meeting data
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")
            attendees_list = [a.strip() for a in attendees.split(",")]

            data_handler.add_meeting(date, time, transcription, topic, attendees_list, summary)
            st.success("Meeting recorded successfully.")
        else:
            st.error("Please provide all required inputs.")



# Directory Structure
#
# project_root/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py  # Streamlit entry point
# │   ├── query_tab.py  # Query tab logic
# │   ├── meeting_tab.py  # Meeting tab logic
# │   ├── utils/
# │   │   ├── __init__.py
# │   │   ├── llm_helper.py  # Interact with LLMs
# │   │   ├── data_handler.py  # Handle JSON data
# │   │   ├── audio_processor.py  # Audio processing logic
# ├── data/
# │   ├── raw_posts.json  # Input data
# │   ├── processed_posts.json  # Enriched data
# ├── requirements.txt
# ├── README.md

# # requirements.txt
# streamlit==1.35.0
# langchain==0.2.14
# langchain-core==0.2.39
# langchain-community==0.2.12
# langchain_groq==0.1.9
# pandas==2.0.2

# app/main.py
# import streamlit as st
# from app.query_tab import render_query_tab
# from app.meeting_tab import render_meeting_tab

# st.set_page_config(page_title="Meeting AI", layout="wide")

# st.sidebar.title("Navigation")
# option = st.sidebar.radio("Select a tab:", ["Query", "Meeting"])

# if option == "Query":
#     render_query_tab()
# elif option == "Meeting":
#     render_meeting_tab()

# # app/query_tab.py
# import streamlit as st
# from app.utils.data_handler import DataHandler
# from app.utils.llm_helper import LLMHelper

# def render_query_tab():
#     st.title("Query Tab")
#     query = st.text_input("Ask a question about your meetings:")

#     if st.button("Search"):
#         data_handler = DataHandler("data/processed_posts.json")
#         related_data = data_handler.get_related_data(query)
#         if related_data:
#             llm = LLMHelper()
#             response = llm.get_response(related_data)
#             st.write(response)
#         else:
#             st.write("No related data found.")

# # app/meeting_tab.py
# import streamlit as st
# from app.utils.audio_processor import process_audio_transcription
# from app.utils.data_handler import DataHandler

# def render_meeting_tab():
#     st.title("Meeting Tab")
#     uploaded_audio = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
#     topic = st.text_input("Conversation Topic")
#     attendees = st.text_area("Attendees (comma-separated)")

#     if st.button("Process Meeting"):
#         if uploaded_audio and topic and attendees:
#             transcript = process_audio_transcription(uploaded_audio)
#             if transcript:
#                 data_handler = DataHandler("data/processed_meetings.json")
#                 data_handler.save_meeting_data(
#                     {
#                         "date": str(st.session_state.get("date")),
#                         "time": str(st.session_state.get("time")),
#                         "conversation": transcript,
#                         "conversation_about": topic,
#                         "attendees": attendees.split(","),
#                     }
#                 )
#                 st.write("Meeting data saved successfully.")
#             else:
#                 st.write("Error processing audio.")

# # app/utils/data_handler.py
# import json

# class DataHandler:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def get_related_data(self, query):
#         with open(self.file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return [item for item in data if query.lower() in item["text"].lower()]

#     def save_meeting_data(self, meeting_data):
#         with open(self.file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         data.append(meeting_data)
#         with open(self.file_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=4)

# # app/utils/llm_helper.py
# from langchain_groq import ChatGroq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class LLMHelper:
#     def __init__(self):
#         self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.2-90b-text-preview")

#     def get_response(self, related_data):
#         prompt = "\n".join([item["text"] for item in related_data])
#         response = self.llm.invoke(prompt)
#         return response.content

# # app/utils/audio_processor.py
# def process_audio_transcription(audio_file):
#     from langchain_groq import AudioGroq
#     import os
#     from dotenv import load_dotenv

#     load_dotenv()
#     audio_llm = AudioGroq(groq_api_key=os.getenv("GROQ_API_KEY"))

#     response = audio_llm.transcribe(audio_file.read())
#     return response.text
