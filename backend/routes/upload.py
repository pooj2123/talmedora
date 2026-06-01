from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import Header

import shutil
import os
import fitz

from services import vector_service

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import (
    Document
)

from database.db import SessionLocal
from database.models import Report
from database.user_model import User

from auth.auth import verify_token

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_file(

    file: UploadFile = File(...),

    description: str = Form(...),

    authorization: str = Header(...)

):

    db = SessionLocal()

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if not payload:

        db.close()

        return {
            "message":
            "Invalid token"
        }

    email = payload["sub"]

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:

        db.close()

        return {
            "message":
            "User not found"
        }

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    doc = fitz.open(file_path)

    text = ""

    for page in doc:

        text += page.get_text()

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    docs = [

        Document(

            page_content=chunk,

            metadata={

                "filename": file.filename,

                "description": description,

                "filepath": file_path,

                "user_id": user.id
            }
        )

        for chunk in chunks
    ]

    vector_service.vectorstore.add_documents(
        docs
    )

    vector_service.vectorstore.save_local(
        "faiss_index"
    )

    report = Report(

        filename=file.filename,

        description=description,

        filepath=file_path,

        user_id=user.id
    )

    db.add(report)

    db.commit()

    db.close()

    return {

        "message":
        "Chunks stored in FAISS vector DB",

        "filename":
        file.filename,

        "description":
        description
    }