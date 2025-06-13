import streamlit as st
import requests

st.set_page_config(page_title="Simple Langgraph ReAct Agent", layout="centered")
st.title("Simple ReAct Agent Chatbot")
st.write("Interact with Chatbot")

system_prompt = st.text_area("Define Agents role: ", height=80, placeholder="Act as a reaserch assitant")

MODEL_NAME = ["llama3-70b-8192", "deepseek-r1-distill-llama-70b", "gemma2-9b-it"]

provider = st.radio("Select model provider: ",("GROQ", "OPENROUTER"))

if provider.lower == "groq":
    selected_model = st.selectbox("Select groq model: ", MODEL_NAME)
else:
    selected_model = st.selectbox("Select openrouter model: ", MODEL_NAME)

allowed_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Ask Something:", height=100, placeholder="Type your question here...")

API_URL = "http://127.0.0.1:8080/chat"

if st.button("🚀 Ask Agent"):
    if user_query.strip():
        with st.spinner("Thinking..."):
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allowed_web_search
            }

            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(f"{response_data['error']}")
                    else:
                        st.success("Agent Responded!")
                        st.markdown(f"**Response:** {response_data['response']}")
                else:
                    st.error("API Error: Backend did not return a 200 OK response.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request Failed: {e}")
    else:
        st.warning("Please type a query before clicking the button.")