from fastapi import FastAPI, HTTPException
from Schema_File.app_schema import ChatRequestSchema
from models_config import allowed_models
from Agents_Folder.agents import get_response_from_ai_agent

app = FastAPI(title="Simple Langgraph agent")

@app.post("/chat")
async def chat_endpoint(request: ChatRequestSchema):
    provider = request.model_provider

    if provider not in allowed_models:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Provider{provider}"
        )
    
    if request.model_name not in allowed_models[provider]:
        allowed = ", ".join(sorted(allowed_models[provider]))
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model: {request.model_name}. allowed models: {allowed}"
        )
    
    llm_id = request.model_name
    user_prompt = "\n ".join(request.messages)
    allowed_search = request.allow_search
    system_prompt = request.system_prompt

    try:
        ai_response = get_response_from_ai_agent(
            llm_id=llm_id,
            query=user_prompt,
            allow_search=allowed_search,
            system_prompt=system_prompt,
            provider=provider,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    return {"response": ai_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8080, reload=True)