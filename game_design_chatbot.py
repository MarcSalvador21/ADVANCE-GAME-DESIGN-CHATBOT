import streamlit as st
from google.genai import Client
import os

# Page setup
st.set_page_config(page_title="Advanced Game Design Chatbot", page_icon="🎮")
st.title("Advanced Game Design Chatbot")

# 1. Get API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    api_key = st.text_input("Enter Google API Key", type="password")

if api_key:
    client = Client(api_key=api_key)

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your Advanced Game Design assistant. Ask me about game engines, level design, mechanics, AI in games, or graphics."
        }
    ]

# 3. Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle new input
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare content for API
    gemini_contents = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Remove initial model greeting if needed
    if gemini_contents and gemini_contents[0]["role"] == "model":
        gemini_contents.pop(0)

    # 5. Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=gemini_contents,
                config={
                    "system_instruction": "You are an expert in Advanced Game Design. Give detailed explanations and practical examples."
                }
            )
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

            # Final message
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
