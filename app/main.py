import streamlit as st
from query.query_main import render_query_tab
from meeting.meeting_main import render_meeting_tab
from users.login import render_login_page
from users.register import render_register_page

st.set_page_config(page_title="Meeting AI", layout="wide")

# Initialize session state for navigation and user session
# if "page" not in st.session_state:
#     st.session_state["page"] = "Login"  # Default to Login page

# Check if the user is logged in
is_logged_in = "user_email" in st.session_state

# Sidebar Navigation (force rerun)
# if is_logged_in:
#     # If the user is logged in, hide Login and Register options
#     option = st.sidebar.radio(
#         "Select a tab:", 
#         ["Query", "Meeting"],  # Only show Query and Meeting tabs
#         index=["Query", "Meeting"].index(st.session_state["page"])
#     )
# else:
#     # If not logged in, show Login and Register options
#     option = st.sidebar.radio(
#         "Select a tab:", 
#         ["Login", "Register"],  # Show Login and Register options
#         index=["Login", "Register"].index(st.session_state["page"])
#     )

# # Update session state based on navigation
# st.session_state["page"] = option

# Render selected page
if st.session_state["page"] == "Query":
    render_query_tab()
elif st.session_state["page"] == "Meeting":
    render_meeting_tab()
elif st.session_state["page"] == "Login":
    render_login_page()
elif st.session_state["page"] == "Register":
    render_register_page()

# Logout functionality when the user is logged in
# if is_logged_in:
if st.sidebar.button("Logout"):
        # Clear session state and redirect to Login page
    st.session_state.clear()
    st.session_state["page"] = "Login"  # Redirect to login page
    st.experimental_rerun()  # Rerun the app to refresh the UI
