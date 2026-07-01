from fastapi import APIRouter
from fastapi import Header

from pydantic import BaseModel

import hashlib
import time

from database.db import SessionLocal
from database.user_model import User

from auth.auth import verify_token

from services import vector_service
from services.gemini_service import (
    generate_response
)

router = APIRouter()

CACHE_TTL_SECONDS = 300
CACHE_MAX_ENTRIES = 100
chat_response_cache = {}


def _make_cache_key(user_id, question, retrieved_text):
    digest = hashlib.sha256(
        f"{user_id}:{question}:{retrieved_text}".encode("utf-8")
    ).hexdigest()
    return f"chat:{user_id}:{digest}"


def _cache_get(key):
    entry = chat_response_cache.get(key)
    if not entry:
        return None

    response, expires_at = entry
    if time.time() > expires_at:
        del chat_response_cache[key]
        return None

    return response


def _cache_set(key, response):
    if len(chat_response_cache) >= CACHE_MAX_ENTRIES:
        oldest_key = min(
            chat_response_cache,
            key=lambda k: chat_response_cache[k][1]
        )
        del chat_response_cache[oldest_key]

    chat_response_cache[key] = (
        response,
        time.time() + CACHE_TTL_SECONDS
    )


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

    retrieved_documents = [
        {
            "filename": doc.metadata.get("filename"),
            "description": doc.metadata.get("description"),
            "summary": doc.metadata.get("summary"),
            "content": doc.page_content[:400]
        }
        for doc in user_docs
    ]

    cache_key = _make_cache_key(
        user.id,
        request.question,
        retrieved_text
    )

    cached_response = _cache_get(cache_key)
    if cached_response is not None:
        return cached_response

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

    response_payload = {

        "question":
        request.question,

        "answer":
        ai_response,

        "retrieved_documents":
        retrieved_documents
    }

    _cache_set(
        cache_key,
        response_payload
    )

    return response_payload