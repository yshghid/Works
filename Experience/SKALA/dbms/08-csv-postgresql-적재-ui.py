# 7. Streamlit UI
import streamlit as st
import requests
import os
from dotenv import load_dotenv

os.chdir("/Users/yshmbid/Documents/home/github/SQL")
load_dotenv() 

st.title("추천 시스템 데모")

user_id = st.text_input("User ID 입력:")

if st.button("추천 받기"):
    response = requests.post("http://localhost:8000/recommend", json={"user_id": user_id})
    st.json(response.json())