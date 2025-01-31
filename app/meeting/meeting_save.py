import requests
import json
import os
import streamlit as st

CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

def generate_meeting_object(transcript):
    prompt = f"Given the meeting transcript, structure it into a JSON object: {transcript}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0}

    response = requests.post(CHATGROQ_API_URL_CHAT, json=payload, headers=headers)
    return json.loads(response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")) if response.status_code == 200 else None

def save_meeting_to_json(meeting_object):
    meetings_file = "data/meetings.json"
    meetings_data = json.load(open(meetings_file, 'r')) if os.path.exists(meetings_file) else []
    meetings_data.append(meeting_object)

    with open(meetings_file, 'w') as f:
        json.dump(meetings_data, f, indent=4)
