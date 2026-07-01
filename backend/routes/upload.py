from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import Header
from fastapi import BackgroundTasks

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


def process_uploaded_report(report_id: int):

    db = SessionLocal()

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    db.close()

    if not report or not os.path.exists(
        report.filepath
    ):
        return

    try:
        doc = fitz.open(report.filepath)

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
                    "filename": report.filename,
                    "description": report.description,
                    "filepath": report.filepath,
                    "user_id": report.user_id,
                    "summary": vector_service.summarize_text(
                        chunk
                    )
                }
            )
            for chunk in chunks
        ]

        vector_service.vectorstore.add_documents(docs)
        vector_service.vectorstore.save_local(
            "faiss_index"
        )

    except Exception as e:
        print(
            "Background upload processing failed:",
            e
        )


@router.post("/upload")
async def upload_file(

    file: UploadFile = File(...),

    description: str = Form(...),

    authorization: str = Header(...),

    background_tasks: BackgroundTasks = BackgroundTasks()

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

    report = Report(

        filename=file.filename,

        description=description,

        filepath=file_path,

        user_id=user.id
    )

    db.add(report)

    db.commit()

    background_tasks.add_task(
        process_uploaded_report,
        report.id
    )

    db.close()

    return {

        "message":
        "Upload successful. Processing will continue in the background.",

        "filename":
        file.filename,

        "description":
        description
    }