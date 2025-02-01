import streamlit as st
from users.database import get_user  # Function to fetch user data

def render_login_page():
    st.title("Login to Meeting AI")

    # Social login buttons (Google & Facebook)
    # st.button("Continue with Google")
    # st.button("Continue with Facebook")

    st.markdown("---")

    # Email & Password Login
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(email, password)  # Check if user exists
        if user:
            st.success("Login successful!")
            # Store email and password in session state
            st.session_state["user_email"] = email
            st.session_state["user_password"] = password  # Optional: Store password (consider security)
            st.session_state["page"] = "Query"  # After login, redirect to Query page or Meeting
        else:
            st.error("Invalid email or password.")

    # Redirect to Register Page
    if st.button("New user? Register here"):
        st.session_state["page"] = "Register"
        st.sidebar.radio("Select a tab:", ["Query", "Meeting", "Login"], index=2)
