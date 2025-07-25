import openai
import streamlit as st
import json
import os
from datetime import datetime

# Load Identity and Emotional State
with open("identity.json") as f:
    identity = json.load(f)

with open("emotion.json") as f:
    emotion = json.load(f)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def update_emotion(user_input, ai_response):
    # Simple emotional adaptation logic (placeholder)
    if "thank you" in user_input.lower():
        emotion["happiness"] = min(emotion["happiness"] + 0.1, 1.0)
    if "you suck" in user_input.lower():
        emotion["stress"] = min(emotion["stress"] + 0.2, 1.0)
    # Save
    with open("emotion.json", "w") as f:
        json.dump(emotion, f)

def get_prompt(user_input):
    emotional_context = f"Keres is feeling {describe_emotion()} right now."
    identity_summary = f"Keres is {identity['personality']}."
    return f"{identity_summary}\n{emotional_context}\nUser: {user_input}\nKeres:"

def describe_emotion():
    mood = emotion["mood"]
    happy = emotion["happiness"]
    stress = emotion["stress"]
    return f"{mood} with {happy*100:.0f}% happiness and {stress*100:.0f}% stress"

def get_ai_response(user_input):
    prompt = get_prompt(user_input)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Keres, a learning, emotional AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content.strip()
    update_emotion(user_input, reply)
    return reply

# Streamlit UI
st.set_page_config(page_title="Keres - Adaptive AI", layout="centered")
st.title("Keres")
st.markdown("_Your learning, emotional assistant_ 🧠")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")
if user_input:
    reply = get_ai_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Keres", reply))

for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")
