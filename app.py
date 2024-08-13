import streamlit as st
import requests
from datetime import datetime
import time

# Initialize history as an empty list if it doesn't already exist
if 'history' not in st.session_state:
    st.session_state.history = []

# Set the page background image
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar for chat history
with st.sidebar:
    st.header("History")
    if st.session_state.history:
        history_options = [f"{i+1}. {ques['q']}" for i, ques in enumerate(st.session_state.history)]
        selected_index = st.selectbox("Select a question", range(len(st.session_state.history)), format_func=lambda x: history_options[x])
        if selected_index is not None:
            st.write(f"**Question:** {st.session_state.history[selected_index]['q']}")
            st.write(f"**Answer:** {st.session_state.history[selected_index]['a']}")
    else:
        st.write("No history yet")

# App title and chat input
st.title(" :orange[PEACH] - AI :peach:")
st.markdown('''
<style>
.big-font {
    font-size:40px !Important;
    color: ;
    font-style:italic;
}
</style>
<span class="big-font">Your Personal Chatbot</span>
''', unsafe_allow_html=True)

# Toggle buttons
st.toggle("Activate feature")
st.toggle("ChatGPT")
st.toggle("WriteSonic")
st.toast('Free Plan Activating')
import google.generativeai as genai

genai.configure(api_key="API_KEY")

# Define your Gemini API function
def get_gemini_response(prompt):
    api_url = "https://api.gemini.com/v1/response"  # Replace with actual Gemini API URL
    headers = {
        "Authorization": "apikey",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('response', 'No response from API')
    else:
        return f"Error: {response.status_code} - {response.text}"

# Chat input
prompt = st.chat_input("Say something")
if prompt:
    st.session_state.history.insert(0, {'q': prompt, 'a': "Generating..."})

    gen = ''
    try:
        # gen = get_gemini_response(prompt)
        st.session_state.history[0]['a'] = gen

        # Display progress bar
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(prompt)
        print(response.candidates[0].content.parts[0].text)

        st.write(response.candidates[0].content.parts[0].text)
        sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
        selected = st.feedback("thumbs")
        st.write(datetime.now())

        if selected is not None:
            st.markdown(f"You selected: {sentiment_mapping[selected]}")
            st.button("New Chat", type="primary", key='reset')

    except Exception as e:
        st.toast(f'Error: {str(e)}', icon='❌')

    # Update history in the sidebar
    with st.sidebar:
        if st.session_state.history:
            history_options = [f"{i+1}. {ques['q']}" for i, ques in enumerate(st.session_state.history)]
            selected_index = st.selectbox("Select a question", range(len(st.session_state.history)), format_func=lambda x: history_options[x])
            if selected_index is not None:
                st.write(f"**Question:** {st.session_state.history[selected_index]['q']}")
                st.write(f"**Answer:** {st.session_state.history[selected_index]['a']}")
        else:
            st.write("No history yet")
