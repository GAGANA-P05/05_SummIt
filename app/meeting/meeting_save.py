import requests
import json
import os
import streamlit as st

CHATGROQ_API_URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

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
