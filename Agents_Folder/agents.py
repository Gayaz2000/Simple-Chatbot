from Logs_Folder.logger_setup import setup_logger
import logging

import requests
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

system_prompt = "Act as an AI chatbot who is smart and friendly"

# Setup logger
logger = setup_logger()
logger.info("🚀 Starting application")

def get_response_from_openrouter(query, system_prompt):
    try:
        url = "https://api.openrouter.ai/v1/complete"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openrouter-llama-3.3-70b",
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}],
            "max_tokens": 100
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error if the response is not successful
        response_data = response.json()

        # Extract and return the AI message content
        ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return ai_message
    except requests.exceptions.RequestException as e:
        print(f"Error with OpenRouter API: {e}")
        return "Error communicating with OpenRouter API."
    

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from Nodes_Folder.nodes import search_tool
    
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenRouter":
        ai_message = get_response_from_openrouter(query, system_prompt)
        return ai_message
    
    # Search tool functionality
    tools = [search_tool] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )

    # Interact with the agent
    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
