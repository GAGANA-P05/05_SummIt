import streamlit as st
from users.database import insert_user  # Function to store user data

def render_register_page():
    st.title("Register for Meeting AI")

    # Social login buttons (Google & Facebook)
    # st.button("Continue with Google")
    # st.button("Continue with Facebook")

    st.markdown("---")

    # User Input Fields
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Insert user data into the database
            insert_user(full_name, email, password)
            st.success("Registration successful! Redirecting to login page...")
            
            # Store user email and password in session after successful registration
            st.session_state["user_email"] = email
            st.session_state["user_password"] = password  # Optional: Store password (consider security)

            # Redirect to the Login page after registration
            st.session_state["page"] = "Login"

            # Sidebar radio forces page update
            st.sidebar.radio("Select a tab:", ["Query", "Meeting", "Login"], index=2)

    # Back to Login
    if st.button("Already have an account? Login here"):
        st.session_state["page"] = "Login"
        st.sidebar.radio("Select a tab:", ["Query", "Meeting", "Login"], index=2)
