from pydantic import BaseModel


class ChatGPTResponse(BaseModel):
    summary: str
    importance: int


def summarize(content: str) -> ChatGPTResponse:
    raise NotImplementedError
