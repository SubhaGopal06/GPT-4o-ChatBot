#importing built-in libraries
import os
import json

#importing other libraries
import streamlit as st
import openai

#configuring openai
working_dir =os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

#
OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

#configuring streamlit page settings
st.set_page_config(
    page_title="GPT-3.5-turbo ChatBot",
    page_icon="💬",
    layout="centered"
)

#initialize chat session in streamlit if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Page title
st.title("🤖 GPT-3.5-turbo CHATBOT")

#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): #user msg, assistant msg
        st.markdown(message["content"]) # given by user or bot

#input field for user message
user_prompt = st.chat_input("Type here...")
if user_prompt:

    #just adds user's question to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    #Getting response from gpt by sending user's msg!
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    #display GPT-3.5's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)