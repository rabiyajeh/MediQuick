
import streamlit as st
import numpy as np
import random
import time
import streamlit as st
import requests
from requests.exceptions import RequestException




API_KEY2 = "api71-api-cccff247-4318-43d0-9f81-35cdb953dd83"
API_URL = "https://api.ai71.ai/v1/chat/completions"


st.title("Medical Chatbot")

# Set a default model (if needed)
if "model_page_2" not in st.session_state:
    st.session_state["model_page_2"] = "medical-assistant-model"

# Function to get response from the medical assistant API
def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY2}",
        "Content-Type": "application/json"
    }
    data = {
        "model": st.session_state["model_page_2"],
        "messages": [
            {"role": "system", "content": "You are a doctor. Provide clear and accurate medical responses based on the symptoms described."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', "No response received.")
    except RequestException as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, there was an error processing your request."

# Initialize chat history
if "messages_page_2" not in st.session_state:
    st.session_state["messages_page_2"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages_page_2"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your medical concern?"):
    # Add user message to chat history
    st.session_state["messages_page_2"].append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the medical assistant API
    response = get_response(prompt)
    # Add assistant response to chat history
    st.session_state["messages_page_2"].append({"role": "assistant", "content": response})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
