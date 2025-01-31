import os
import requests
import json
import streamlit as st

CHATGROQ_API_URL_TRANSCRIBE = "https://api.groq.com/openai/v1/audio/transcriptions"
CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        st.error("Audio file not found!")
        return None

    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"model": "whisper-large-v3", "response_format": "json", "temperature": 0}
        headers = {"Authorization": f"Bearer {API_KEY}"}

        response = requests.post(CHATGROQ_API_URL_TRANSCRIBE, files=files, data=data, headers=headers)

    return response.json().get("text", "") if response.status_code == 200 else None

def get_realtime_insights(transcript_chunk):
    prompt = f"Analyze this meeting excerpt: {transcript_chunk}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0}

    response = requests.post(CHATGROQ_API_URL_CHAT, json=payload, headers=headers)
    return json.loads(response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")) if response.status_code == 200 else None
