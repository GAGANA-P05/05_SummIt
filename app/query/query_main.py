import streamlit as st
import json
from query.data_handler import DataHandler
from query.llm_helper import LLMHelper

def render_query_tab():
    st.title("Query Tab")
    query = st.text_input("Ask a question about your meetings:")

    if st.button("Search"):
        data_handler = DataHandler("data/meetings.json")
        llm_helper = LLMHelper()

        relevant_data = data_handler.get_relevant_data(query)
        if not relevant_data:
            st.write("No relevant meeting found.")
            return
        
        # Generate explanation
        explanation_prompt = (
            f"Here is the most relevant meeting data:\n"
            f"{json.dumps(relevant_data, indent=2)}\n\n"
            "Provide a summary of this meeting, explain its meaning, and suggest actionable items or follow-up steps."
        )
        explanation = llm_helper.get_response(explanation_prompt)

        # Display results
        st.subheader("Relevant Meeting Data:")
        st.json(relevant_data)
        st.download_button("Download Relevant Data", json.dumps(relevant_data, indent=2), "relevant_meeting_data.json", "application/json")

        st.subheader("Explanation and Suggestions:")
        st.write(explanation)
        st.download_button("Download Explanation", explanation, "explanation.txt", "text/plain")



# Streamlit App Execution
if __name__ == "__main__":
    render_query_tab()
