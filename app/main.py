
from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.orchestrator import SHLRecommendationAgent


app = FastAPI()

agent = SHLRecommendationAgent()


class Message(BaseModel):

    role: str
    content: str


class ChatRequest(BaseModel):

    messages: list[Message]


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        print(request.messages)

        converted = [
            message.model_dump()
            for message in request.messages
        ]

        print(converted)

        response = agent.handle_conversation(
            [message.model_dump() for message in request.messages]
        )

        return response

    except Exception as e:

        return {
            "error": str(e)
        }

