import streamlit as st

# Set up the page config
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

# Step 1: System prompt and model selection on top
with st.container():
    system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

    # Create a row with model provider and model selection on top
    provider = st.radio("Select Provider:", ("Groq", "OpenAI", "ollama"))
    
    if provider == "Groq":
        selected_model = st.selectbox("Select Groq Model:", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    elif provider == "OpenAI":
        selected_model = st.selectbox("Select OpenAI Model:", ["gpt-4o-mini"])
    elif provider == "ollama":
        selected_model = st.selectbox("Select OpenAI Model:", ["llama3.2:1b"])

# Step 2: Query section
st.subheader("Ask Your AI Agent")
user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

# Option to allow web search
allow_web_search = st.checkbox("Allow Web Search")

# API URL
API_URL = "http://127.0.0.1:45555/chat"

# Button to submit the query
if st.button("Ask Agent!"):
    if user_query.strip():
        # Step 3: Connect with backend via URL
        import requests

        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }
        print(payload)
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")
        else:
            st.error(f"Error: {response.status_code}")
