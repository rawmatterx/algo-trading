import streamlit as st
from utils.auth import UpstoxAuth
import time

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
        .debug-info {
            font-size: 12px;
            color: #666;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'auth_message' not in st.session_state:
        st.session_state.auth_message = None

def main():
    init_session_state()
    auth = UpstoxAuth()
    
    # Center-aligned title
    st.markdown("<h1 style='text-align: center;'>🤖 Algo Trading</h1>", unsafe_allow_html=True)
    
    # Handle OAuth callback
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        auth_code = query_params["code"][0]
        with st.spinner("Authenticating..."):
            token = auth.get_access_token(auth_code)
            if token:
                st.session_state.access_token = token
                st.session_state.authentication_status = "success"
                st.session_state.auth_message = "Successfully authenticated!"
                # Clear URL parameters
                st.experimental_set_query_params()
                time.sleep(1)  # Brief pause for better UX
                st.rerun()
            else:
                st.session_state.authentication_status = "failed"
                st.session_state.auth_message = "Authentication failed. Please try again."
    
    # Display authentication status message if any
    if st.session_state.auth_message:
        if st.session_state.authentication_status == "success":
            st.success(st.session_state.auth_message)
        else:
            st.error(st.session_state.auth_message)
        # Clear the message after displaying
        st.session_state.auth_message = None
    
    # Main interface
    if "access_token" not in st.session_state:
        st.markdown("""
            <div style='text-align: center; margin: 2rem 0;'>
                <p style='color: #666; margin-bottom: 2rem;'>
                    Connect your Upstox account to start trading
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Login with Upstox", key="login_button"):
            login_url = auth.get_login_url()
            st.markdown(f'<meta http-equiv="refresh" content="0;url={login_url}">', unsafe_allow_html=True)
            
    else:
        # Get and display user profile
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
        else:
            st.error("Failed to load profile. Please try logging in again.")
            if st.button("Retry Login"):
                auth.logout()
                st.rerun()

    # Add debug information in development
    if not auth._is_streamlit_cloud():
        with st.expander("Debug Information"):
            st.markdown(f"""
                - Redirect URI: `{auth.redirect_uri}`
                - Environment: {'Streamlit Cloud' if auth._is_streamlit_cloud() else 'Local'}
                - Session State Keys: {list(st.session_state.keys())}
            """)

if __name__ == "__main__":
    main()