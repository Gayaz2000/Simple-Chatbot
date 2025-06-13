from pydantic import BaseModel, Field
from typing_extensions import List

class ChatRequestSchema(BaseModel):
    model_name : str = Field(..., examples=["gemma2-9b-it", "deepseek-r1-distill-llama-70b"])
    model_provider : str = Field(..., examples=["Groq"])
    system_prompt : str = Field(..., default=["You are an friendly and helpful assistant"])
    messages : List[str] = Field(..., examples=["Hi, How can I help you"])
    allow_search : bool = Field(..., default=False)