import os
import requests
import json
import streamlit as st

CHATGROQ_API_URL_TRANSCRIBE = "https://api.groq.com/openai/v1/audio/transcriptions"
CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

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
