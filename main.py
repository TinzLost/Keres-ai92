import streamlit as st
import requests
import os

# Get your Hugging Face API key from Streamlit secrets
HF_API_KEY = os.getenv("HF_API_KEY")

# Set up Streamlit page
st.set_page_config(page_title="Keres", page_icon="🧠")
st.title("Keres")
st.caption("Your learning, emotional assistant 🧠")

# Get user input
user_input = st.text_input("You:", "")

# Function to call Hugging Face model
def get_ai_response(user_input):
    if not HF_API_KEY:
        return "⚠️ Hugging Face API key is missing. Please check your secrets config."

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": f"User: {user_input}\nAssistant:",
        "parameters": {
            "max_new_tokens": 150,
            "do_sample": True,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            headers=headers,
            json=payload
        )
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return f"⚠️ HF API Error: {result['error']}"

        text = result[0]["generated_text"]
        reply = text.split("Assistant:")[-1].strip()
        return reply

    except Exception as e:
        return f"⚠️ Error connecting to Hugging Face API: {str(e)}"

# Only generate a response if the user types something
if user_input:
    reply = get_ai_response(user_input)
    st.markdown(f"**Keres:** {reply}")
