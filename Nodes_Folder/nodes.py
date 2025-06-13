# module_b/b_core.py
import logging
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from Schema_File.state_schemas import State

logger = logging.getLogger(__name__)

search_tool = DuckDuckGoSearchRun(max_results=2)
tools = [search_tool]

llm = ChatGroq(model="gemma2-9b-it")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def do_something_b():
    logger.warning("This is a warning from Module B")
    logger.info("Doing something awesome in Module B")