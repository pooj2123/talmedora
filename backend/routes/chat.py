from fastapi import APIRouter
from fastapi import Header

from pydantic import BaseModel

from database.db import SessionLocal
from database.user_model import User

from auth.auth import verify_token

from services import vector_service
from services.gemini_service import (
    generate_response
)

router = APIRouter()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")
async def chat(

    request: ChatRequest,

    authorization: str = Header(...)

):

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if not payload:

        return {
            "error":
            "Invalid token"
        }

    email = payload["sub"]

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    db.close()

    if not user:

        return {
            "error":
            "User not found"
        }

    results = vector_service.vectorstore.similarity_search(
        request.question,
        k=20
    )

    user_docs = [

        doc

        for doc in results

        if doc.metadata.get(
            "user_id"
        ) == user.id
    ]

    if len(user_docs) == 0:

        return {
            "question":
            request.question,

            "answer":
            "No relevant information found in your uploaded reports."
        }

    retrieved_text = "\n\n".join(

        [
            doc.page_content

            for doc in user_docs
        ]
    )

    try:

        ai_response = generate_response(

            retrieved_text,

            request.question
        )

    except Exception as e:

        print(
            "LLM Error:",
            e
        )

        ai_response = (

            "AI response generation is currently unavailable.\n\n"

            + retrieved_text[:1500]
        )

    return {

        "question":
        request.question,

        "answer":
        ai_response
    }