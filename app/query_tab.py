import streamlit as st
import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Initialize the sentence transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

import os
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# class DataHandler:
#     def __init__(self, file_path, model_name="all-MiniLM-L6-v2"):
#         self.file_path = file_path
#         self.model = SentenceTransformer(model_name)  # Load the embedding model

#     def get_related_data(self, query):
#         # Check if the file exists and is not empty
#         if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
#             with open(self.file_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)

#             # Extract transcript texts
#             transcripts = []
#             transcript_to_data_map = []

#             for item in data:
#                 if "transcript" in item:
#                     for transcript_item in item["transcript"]:
#                         if "text" in transcript_item:
#                             transcripts.append(transcript_item["text"])
#                             transcript_to_data_map.append(item)  # Maintain a mapping to the original data

#             if not transcripts:
#                 return None  # No transcripts available

#             # Compute embeddings for all transcript texts
#             transcript_embeddings = self.model.encode(transcripts)

#             # Compute the embedding for the query
#             query_embedding = self.model.encode([query])[0]

#             # Calculate cosine similarities between query embedding and transcript embeddings
#             similarities = cosine_similarity([query_embedding], transcript_embeddings)[0]

#             # Find the most related transcript index
#             max_similarity_index = similarities.argmax()
#             max_similarity_score = similarities[max_similarity_index]

#             # Define a similarity threshold for relevance
#             threshold = 0.5

#             if max_similarity_score > threshold:
#                 # Return the most relevant data
#                 return transcript_to_data_map[max_similarity_index]
#             else:
#                 return None  # No relevant data found
#         else:
#             return None  # File doesn't exist or is empty
# # turn an empty list if the file is empty


import os
import json
import streamlit as st
  # Replace with actual ChatGroq SDK import


class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.llm_helper = LLMHelper()

    def get_relevant_data_and_explanation(self, query):
        # Step 1: Read and check JSON file
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Step 2: Create a prompt to ask ChatGroq to find the most relevant data
            selection_prompt = (
                               f"Here is the data from various meetings. Find the one most relevant to this query: '{query}'. "
                               "Return only the relevant object in valid JSON format, with no preamble, comments, or explanation.\n\nData:\n"
                )
            selection_prompt += json.dumps(data, indent=2)

# Step 3: Get the most relevant data using ChatGroq
            relevant_data_json = self.llm_helper.get_response(selection_prompt)
            print("Relevant Data (JSON object):", relevant_data_json)


            # Parse the response to JSON
            try:
                relevant_data = json.loads(relevant_data_json)
            except json.JSONDecodeError:
                return {"error": "Failed to parse the relevant data response."}

            # Step 4: Create a follow-up prompt for explanation and suggestions
            explanation_prompt = (
                "Here is the most relevant meeting data:\n"
                f"{json.dumps(relevant_data, indent=2)}\n\n"
                "Provide a summary of this meeting, explain its meaning, and suggest actionable items or follow-up steps."
            )

            explanation_response = self.llm_helper.get_response(explanation_prompt)

            return {"relevant_data": relevant_data, "explanation": explanation_response}
        else:
            return {"error": "The JSON file is empty or does not exist."}


class LLMHelper:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def get_response(self, prompt):
        # Send the prompt to ChatGroq and return the response
        response = self.llm.invoke(prompt)
        return response.content


def render_query_tab():
    st.title("Query Tab")
    query = st.text_input("Ask a question about your meetings:")

    if st.button("Search"):
        # Initialize DataHandler with the path to the JSON file
        data_handler = DataHandler("data/meetings.json")
        
        # Get relevant data and its explanation based on the user's query
        result = data_handler.get_relevant_data_and_explanation(query)
        
        if "error" in result:
            st.write(result["error"])
        else:
            # Display the relevant data
            st.subheader("Relevant Meeting Data:")
            st.json(result["relevant_data"])

            # Display the explanation and suggestions
            st.subheader("Explanation and Suggestions:")
            st.write(result["explanation"])


# Streamlit App Execution
if __name__ == "__main__":
    render_query_tab()
