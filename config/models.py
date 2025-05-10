from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union


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

    model_config = ConfigDict(extra="allow")


class ChatStreamlitRequest(BaseModel):
    text: Optional[str]
    stream: Optional[bool] = False
    model_config = ConfigDict(extra="allow")


class GetDataRequest(BaseModel):
    run: Optional[bool] = True
