import streamlit as st
import os

# Load the climate change knowledge base
@st.cache_data
def load_text_file():
    file_path = "Climate_change.txt"
    if not os.path.exists(file_path):
        return "Error: Climate_change.txt file not found."
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

book_text = load_text_file()

# Split the text into paragraphs for better matching
paragraphs = [p.strip() for p in book_text.split("\n\n") if p.strip() and len(p.strip()) > 100]

# Simple keyword matching response function
def get_response(user_input):
    user_input = user_input.lower()
    matches = [p for p in paragraphs if any(word in p.lower() for word in user_input.split())]
    if matches:
        return matches[0][:2000]  # Limit to 2000 characters per response
    else:
        return "Sorry, I couldn't find relevant information in the document."

# Streamlit UI
st.title("🌍 Climate Change Chatbot")
st.write("Ask me anything about climate change based on the loaded text file.")

if isinstance(book_text, str) and book_text.startswith("Error:"):
    st.error(book_text)
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your climate question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
