import streamlit as st
import requests
import json
from pathlib import Path
import yaml

class UpstoxAuth:
    def __init__(self):
        self.base_url = "https://api.upstox.com/v2"
        self.api_key = st.secrets["UPSTOX_API_KEY"]
        self.api_secret = st.secrets["UPSTOX_API_SECRET"]
        
        # Set redirect URI based on environment
        is_cloud = self._is_streamlit_cloud()
        if is_cloud:
            self.redirect_uri = f"https://{st.secrets.get('STREAMLIT_URL')}"
        else:
            self.redirect_uri = "http://localhost:8501"

    def _is_streamlit_cloud(self):
        """Check if the app is running on Streamlit Cloud"""
        return st.secrets.get('STREAMLIT_URL') is not None

    def get_login_url(self):
        """Generate Upstox login URL"""
        params = {
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        return f"{self.base_url}/login/authorization/dialog?" + "&".join(f"{k}={v}" for k, v in params.items())

    def redirect_to_upstox(self):
        """Redirect to Upstox login page"""
        login_url = self.get_login_url()
        st.markdown(f'<meta http-equiv="refresh" content="0;url={login_url}">', unsafe_allow_html=True)

    def get_access_token(self, auth_code):
        """Exchange authorization code for access token"""
        try:
            response = requests.post(
                f"{self.base_url}/login/authorization/token",
                data={
                    "code": auth_code,
                    "client_id": self.api_key,
                    "client_secret": self.api_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    st.session_state.access_token = token
                    return token
            
            st.error(f"Authentication failed: {response.json().get('message', 'Unknown error')}")
            return None
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None

    def is_authenticated(self):
        """Check if user is authenticated"""
        return bool(st.session_state.get("access_token"))

    def get_user_profile(self):
        """Get authenticated user's profile"""
        if not self.is_authenticated():
            return None

        try:
            response = requests.get(
                f"{self.base_url}/user/profile",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return response.json().get("data", {})
            return None
        except Exception as e:
            st.error(f"Error fetching profile: {str(e)}")
            return None

    def get_headers(self):
        """Get authentication headers"""
        return {
            "Authorization": f"Bearer {st.session_state.access_token}",
            "Content-Type": "application/json"
        }

    def logout(self):
        """Clear authentication data"""
        if "access_token" in st.session_state:
            del st.session_state.access_token