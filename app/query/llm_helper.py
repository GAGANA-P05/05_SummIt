import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMHelper:
    """Helper class to interact with ChatGroq's Llama3 model."""
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def get_response(self, prompt):
        """Send the prompt to ChatGroq and return the response."""
        response = self.llm.invoke(prompt)
        return response.content  # Extract and return the response content
