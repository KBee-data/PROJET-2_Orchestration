# app_front/pages/0_insert.py
import streamlit as st
import requests 
import pandas as pd

session = requests.Session()
API_INSERT = 

st.title("Insert new data")

st. text_input(label="Type information to add to database.", max_chars=500)

if st.button("Send", help="Type information and press enter."):
    try:
        response = session.get(API_INSERT)
        if response.status_code == 200:
            st.write("Data sent")
        #    return True
            response.
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