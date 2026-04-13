# app_front/pages/0_insert.py
import streamlit as st
import requests 
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

session = requests.Session()
API_URL = os.getenv("API_URL")
API_INSERT = f"{API_URL}/data"

if API_URL is None:
    st.error("API_URL is not set. Check the .env file.")

st.title("Insert new data")

user_text = st.text_input(label="Type information to add to database.", max_chars=500)

if st.button("Send", help="Type information and press enter."):
    if not user_text:
        st.warning("Please type something before sending.")
    try:
        response = session.post(API_INSERT, json={"text": user_text})
        if response.status_code == 200:
            st.success("Data sent")
        #    return True
            # st.write(response.json())
        else:
            print(f"Warning: {API_INSERT} returned status code {response.status_code}")
           # return False
        
    except requests.exceptions.Timeout:
        print(f"Error: Request to {API_INSERT} timed out.")
       # return False
    
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {API_INSERT}.")
       # return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error: An unexpected error occured: {e}")
      # return False