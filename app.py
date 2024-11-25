import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Build the Azure OpenAI API endpoint
AZURE_OPENAI_CHAT_ENDPOINT = 'https://thabo-m3mjpcjc-eastus2.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview'

# Sidebar Configuration
with st.sidebar:
    st.title("🤖💬 Azure OpenAI Chatbot")
    
    # Display current configurations
    st.markdown(f"**Deployment Name:** `{AZURE_OPENAI_DEPLOYMENT}`")
    st.markdown(f"**Endpoint:** `{AZURE_OPENAI_ENDPOINT}`")
    
    # Display connection status
    if AZURE_OPENAI_API_KEY:
        st.success("Connected to Azure OpenAI Service", icon="✅")
    else:
        st.error("API Key is missing!", icon="❌")

# Initialize session state for storing chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant created to help users with a variety of tasks, "
                "including answering questions, providing explanations, and offering guidance. "
                "Respond in a friendly and professional tone."
            )
        }  # Default system message
    ]

# Display previous messages, excluding the system message
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to get completion from Azure OpenAI
def get_chat_completion(messages):
    """Get a response from Azure OpenAI API."""
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    payload = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(AZURE_OPENAI_CHAT_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

# Input new prompt
if prompt := st.chat_input("What is up?"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Azure OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Make API call to Azure OpenAI
            response_data = get_chat_completion(st.session_state.messages)
            full_response = response_data["choices"][0]["message"]["content"]
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Store assistant's response in session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
