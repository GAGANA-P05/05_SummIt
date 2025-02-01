import streamlit as st
from query.query_main import render_query_tab
from meeting.meeting_main import render_meeting_tab
from users.login import render_login_page
from users.register import render_register_page

st.set_page_config(page_title="Meeting AI", layout="wide")

# Sidebar Navigation
options = ["Query", "Meeting", "Login", "Register", "Logout"]
option = st.sidebar.radio("Select a tab:", options)

# Page Routing
if option == "Query":
    render_query_tab()
elif option == "Meeting":
    render_meeting_tab()
elif option == "Login":
    render_login_page()
elif option == "Register":
    render_register_page()
elif option == "Logout":
    st.sidebar.success("You have logged out.")
