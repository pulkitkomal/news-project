import asyncio
import json
import os
import uvicorn
from typing import Optional, List, Union

from services.openai_service import OpenAIService
from config.configs import settings
from config.log import logger
from main import get_context, get_data

from pydantic import BaseModel, Field, ConfigDict
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder


openai_obj = OpenAIService(OPENAI_API_KEY=settings.openai_api_key)
app = FastAPI(title="OpenAI-compatible API")

# Data models
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "mock-gpt-model"
    messages: Optional[List[Message]]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False
    text: Optional[str]

    model_config = ConfigDict(extra='allow')

class ChatStreamlitRequest(BaseModel):
    text: Optional[str]
    stream: Optional[bool] = False
    model_config = ConfigDict(extra='allow')

class GetDataRequest(BaseModel):
    run: Optional[bool] = True


def convert_to_input_chat(messages: List[Message]):
    converted_messages = []
    for message in messages:
        if message.role == "user":
            converted_messages.append(message.content)
        else:
            continue
    return ' '.join(converted_messages)


async def _resp_async_generator(messages: List[Message], model: str, max_tokens: int, temperature: float):
    input_message = convert_to_input_chat(messages)
    keywords = await openai_obj.get_keywords(text=input_message)
    context = get_context(keywords, settings.mongo_uri, settings.db_name)
    response = await openai_obj.generate_response(text=input_message, context=context)
    # Iterate over the response synchronously
    for chunk in response.split('.'):
        formatted_chunk = {
            "event":"on_message_delta",
            "data":
                {
                    "id": "step_l7HhkKjDDRPpRk4O9Covm",
                    "delta": {"content":[{"type":"text","text":chunk}]
                }
        }
        }
        yield f"data: {json.dumps(formatted_chunk)}\n\n"
        await asyncio.sleep(0.01)  # Small delay to simulate streaming behavior
    yield "data: [DONE]\n\n"


async def _resp(text: str):
    input_message = text
    keywords = await openai_obj.get_keywords(text=input_message)
    context = get_context(keywords, settings.mongo_uri, settings.db_name)
    response = await openai_obj.generate_response(text=input_message, context=context)

    return response, keywords
        

@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.messages and request.stream:
        return StreamingResponse(
            _resp_async_generator(
                messages=request.messages,
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
        )
    elif request.text and not request.stream:
        response, keywords = await _resp(
                messages=request.text
            )
        logger.info(response)
        return JSONResponse(jsonable_encoder({"response":response, "keywords":keywords}))
    else:
        return HTTPException(status_code=400, detail="No messages provided")


@app.post("/chat/streamlit")
async def chat_streamlit(request: ChatStreamlitRequest):
    if request.text and not request.stream:
        response, keywords = await _resp(
                text=request.text
            )
        logger.info(response)
        return JSONResponse(jsonable_encoder({"response":response, "keywords":keywords}))
    else:
        return HTTPException(status_code=400, detail="No messages provided")


@app.post("/update_data")
async def update_data(request: GetDataRequest):
    rss_feeds = settings.rss_feeds.split(", ")
    get_data(rss_feeds, settings.mongo_uri, settings.db_name)

    return "Data Updated"
   

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

