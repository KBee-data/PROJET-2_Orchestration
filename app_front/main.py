import streamlit as st
import requests
# from frontend_logger import get_logger

APP_API_URL = "http://app_api:8000/"

st.title("MLOps Project 2 - API Ping")

st.subheader("Checking the API")

if st.button("Ping the API route"):
    # logger.info("User clicked the Ping API button")
    try:
        response = requests.get(APP_API_URL)
        if response.status_code == 200:
            st.success(f"API is up! Status code {response.status_code}")
            st.code(f"HTTP status: {response.status_code}")
        else:
            st.error(f"API responded with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to reach API: {e}")
