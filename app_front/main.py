import streamlit as st
import requests

st.title('MLOps Project 2 - API Ping')

APP_API_URL = "http://app_api:8000/health"

try:
    response = requests.get(APP_API_URL)
    if response.status_code == 200:
        st.success(f"API is up! Status code {response.status_code}")
    else:
        st.error(f"API responded with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Failed to reach API: {e}")