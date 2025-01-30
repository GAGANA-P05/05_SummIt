import os
import json
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_groq import ChatGroq # Ensure you have ChatGroq installed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Lightweight model
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")  # Persistent ChromaDB
        self.collection = self.chroma_client.get_or_create_collection(name="meeting_data")
        self.llm_helper = LLMHelper()  # Initialize LLMHelper for real LLM responses

        # Only initialize embeddings if the database is empty
        if self.collection.count() == 0:
            self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Load meeting data and store embeddings in ChromaDB (only runs once)."""
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert all meeting data into vectorized format and store in ChromaDB
            embeddings = []
            metadatas = []
            ids = []

            for idx, meeting in enumerate(data):
                text_representation = json.dumps(meeting)  # Convert meeting data to text
                vector = self.embedding_model.encode(text_representation).tolist()

                embeddings.append(vector)
                metadatas.append({"meeting": text_representation})
                ids.append(str(idx))

            # Store in ChromaDB
            self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
            print(f"✅ {len(data)} meetings embedded and stored in ChromaDB")

    def get_relevant_data_and_explanation(self, query):
        """Retrieve relevant meeting data using vector search and generate an explanation."""
        query_vector = self.embedding_model.encode(query).tolist()

        # Retrieve most relevant meeting using ChromaDB
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=1  # Retrieve top 1 match
        )

        if results['ids'][0]:  # If a result is found
            relevant_data = json.loads(results['metadatas'][0][0]['meeting'])

            # Generate explanation using LLM
            explanation_prompt = (
                f"Here is the most relevant meeting data:\n"
                f"{json.dumps(relevant_data, indent=2)}\n\n"
                "Provide a summary of this meeting, explain its meaning, and suggest actionable items or follow-up steps."
            )

            explanation_response = self.llm_helper.get_response(explanation_prompt)  # Use real LLM response

            return {"relevant_data": relevant_data, "explanation": explanation_response}
        else:
            return {"error": "No relevant meeting found."}


class LLMHelper:
    """Helper class to interact with ChatGroq's Llama3 model."""
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def get_response(self, prompt):
        """Send the prompt to ChatGroq and return the response."""
        response = self.llm.invoke(prompt)
        return response.content  # Extract and return the response content

def render_query_tab():
    st.title("Query Tab")
    query = st.text_input("Ask a question about your meetings:")

    if st.button("Search"):
        # Initialize DataHandler with the path to the JSON file
        data_handler = DataHandler("data/meetings.json")

        # Get relevant data and explanation
        result = data_handler.get_relevant_data_and_explanation(query)

        if "error" in result:
            st.write(result["error"])
        else:
            # Display relevant data
            st.subheader("Relevant Meeting Data:")
            relevant_data_text = json.dumps(result["relevant_data"], indent=2)
            st.json(result["relevant_data"])

            # Download button for relevant data
            st.download_button(
                label="Download Relevant Data",
                data=relevant_data_text,
                file_name="relevant_meeting_data.json",
                mime="application/json"
            )

            # Display explanation and suggestions
            st.subheader("Explanation and Suggestions:")
            explanation_text = result["explanation"]
            st.write(explanation_text)

            # Download button for explanation
            st.download_button(
                label="Download Explanation",
                data=explanation_text,
                file_name="explanation.txt",
                mime="text/plain"
            )


# Streamlit App Execution
if __name__ == "__main__":
    render_query_tab()
