import streamlit as st
from query_tab import render_query_tab
from meeting_tab import render_meeting_tab

st.set_page_config(page_title="Meeting AI", layout="wide")

st.sidebar.title("Navigation")
option = st.sidebar.radio("Select a tab:", ["Query", "Meeting"])

if option == "Query":
    render_query_tab()
elif option == "Meeting":
    render_meeting_tab()
