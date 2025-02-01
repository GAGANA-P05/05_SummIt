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
    """
    Generates real-time insights, suggestions, and improvements based on a meeting transcript chunk.
    Returns a natural language response (no JSON).
    """
    prompt = (
        f"Here is a recent chunk of the meeting transcript:transcript starts here : \n\n{transcript_chunk}\n\n"
        "transcript ends here"
      
        "If the given data  really needs some corrections or suggestions please provide it as soon as possible by analysing current trend within three points"
        "i am going to display your response in on going meeting , so think wisely and respond , if there you really required your response then only respond"
        "if you are not sure about the response then you can skip this question"
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
            try:
                # Extract the content from the API response
                insights = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return insights
            except Exception as e:
                st.error(f"Error parsing API response: {e}")
                return None
        else:
            st.error(f"ChatGroq API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting real-time insights: {e}")
        return None
