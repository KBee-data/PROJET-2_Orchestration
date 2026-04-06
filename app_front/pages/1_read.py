# app_front/pages/1_read.py

import streamlit as st
import pandas as pd
import requests
import os

session=requests.Session()
API_URL=os.getenv("API_URL")
API_READ=f"{API_URL}/read"

if API_URL is None:
    st.error("API is not not set. Check .env file.")

st.title("Display Data")

if st.button("Display data"):
    try:
        response = session.get(API_READ)

        if response.status_code==200:
            st.success("Data retrieved")

            data = response.json()
            df = pd.DataFrame(data)
            st.dataframe(df)

        else:
            st.error(f"Warning: {API_READ} returned status code {response.status_code}")
    
    except requests.exceptions.Timeout:
        st.error(f"Error: Request to {API_READ} timed out.")

    except requests.exceptions.ConnectionError:
        st.error(f"Error: Could not connect to {API_READ}.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Unexpected error: {e}")
        
            