import streamlit as st
import requests
import os

class UpstoxAuth:
    def __init__(self):
        self.base_url = "https://api.upstox.com/v2"
        self.api_key = st.secrets["UPSTOX_API_KEY"]
        self.api_secret = st.secrets["UPSTOX_API_SECRET"]
        
        # Determine if we're running on Streamlit Cloud or locally
        if self._is_streamlit_cloud():
            self.redirect_uri = f"https://{st.secrets['STREAMLIT_HOSTNAME']}"
        else:
            self.redirect_uri = "http://localhost:8501"

    def _is_streamlit_cloud(self):
        """Check if we're running on Streamlit Cloud"""
        return 'STREAMLIT_HOSTNAME' in st.secrets

    def get_login_url(self):
        """Generate Upstox login URL with proper redirect"""
        params = {
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.base_url}/login/authorization/dialog?{query_string}"

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
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    return data["access_token"]
            
            st.error(f"Authentication failed: {response.text}")
            return None
            
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None

    def get_user_profile(self):
        """Get authenticated user's profile"""
        if not st.session_state.get("access_token"):
            return None

        try:
            response = requests.get(
                f"{self.base_url}/user/profile",
                headers={
                    "Authorization": f"Bearer {st.session_state.access_token}",
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                return response.json().get("data", {})
            
            if response.status_code == 401:
                # Token expired or invalid
                st.session_state.pop("access_token", None)
                st.rerun()
                
            return None
        except Exception as e:
            st.error(f"Error fetching profile: {str(e)}")
            return None

    def logout(self):
        """Clear authentication data"""
        if "access_token" in st.session_state:
            del st.session_state.access_token
        if "user_profile" in st.session_state:
            del st.session_state.user_profile