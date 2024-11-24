import streamlit as st
from utils.auth import UpstoxAuth
import yaml
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Algo Trading | Login",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .success-msg {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            color: #155724;
            margin: 1rem 0;
        }
        .error-msg {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f8d7da;
            color: #721c24;
            margin: 1rem 0;
        }
        .stDeployButton {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize authentication
auth = UpstoxAuth()

def main():
    # Center-aligned title with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://assets-netstorage.groww.in/stock-assets/logos/UPLG857753.png", width=200)
        st.markdown("<h1 style='text-align: center;'>Algo Trading</h1>", unsafe_allow_html=True)

    # Handle OAuth callback
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        auth_code = query_params["code"][0]
        with st.spinner("Authenticating..."):
            token = auth.get_access_token(auth_code)
            if token:
                st.session_state.access_token = token
                st.experimental_set_query_params()  # Clear URL parameters
                st.success("Successfully logged in!")
                st.rerun()

    # Check authentication status
    if not auth.is_authenticated():
        st.markdown("""
            <div style='text-align: center; margin: 2rem 0;'>
                <p style='color: #666; margin-bottom: 2rem;'>
                    Connect your Upstox account to start trading
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Login with Upstox", key="login_button"):
            auth.redirect_to_upstox()
    else:
        # Display user profile
        profile = auth.get_user_profile()
        if profile:
            st.markdown(f"""
                <div style='
                    background-color: #f8f9fa;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    margin: 1rem 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                '>
                    <h3 style='margin-bottom: 1rem; color: #333;'>Welcome back! 👋</h3>
                    <p><strong>Name:</strong> {profile.get('name', 'N/A')}</p>
                    <p><strong>Email:</strong> {profile.get('email', 'N/A')}</p>
                    <p><strong>User ID:</strong> {profile.get('user_id', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Go to Dashboard →"):
                st.switch_page("pages/01_Dashboard.py")

            if st.button("Logout"):
                auth.logout()
                st.rerun()

if __name__ == "__main__":
    main()