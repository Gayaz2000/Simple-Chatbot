from typing import Annotated

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]