import os
import re

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

import fitz

from database.db import SessionLocal
from database.models import Report


embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

FAISS_PATH = "faiss_index"


def summarize_text(text, max_chars=240):
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    summary_parts = []
    total = 0

    for sentence in sentences:
        if total + len(sentence) <= max_chars:
            summary_parts.append(sentence)
            total += len(sentence) + 1
        else:
            break

    summary = " ".join(summary_parts).strip()
    if not summary:
        summary = cleaned[:max_chars].rstrip()

    if len(summary) < len(cleaned):
        summary = summary.rstrip(" .,!?:;") + "..."

    return summary


if os.path.exists(FAISS_PATH):

    vectorstore = FAISS.load_local(
        FAISS_PATH,
        embedding_function,
        allow_dangerous_deserialization=True
    )

else:

    vectorstore = FAISS.from_texts(
        ["Initial medical document"],
        embedding_function
    )

    vectorstore.save_local(
        FAISS_PATH
    )


def rebuild_vectorstore():

    global vectorstore

    db = SessionLocal()

    reports = db.query(
        Report
    ).all()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    all_docs = []

    for report in reports:

        if not os.path.exists(
            report.filepath
        ):
            continue

        pdf = fitz.open(
            report.filepath
        )

        text = ""

        for page in pdf:

            text += page.get_text()

        chunks = splitter.split_text(
            text
        )

        docs = [

            Document(
                page_content=chunk,

                metadata={

                    "filename":
                    report.filename,

                    "description":
                    report.description,

                    "filepath":
                    report.filepath,

                    "user_id":
                    report.user_id,

                    "summary":
                    summarize_text(chunk)
                }
            )

            for chunk in chunks
        ]

        all_docs.extend(
            docs
        )

    if len(all_docs) == 0:

        vectorstore = FAISS.from_texts(
            ["Empty medical database"],
            embedding_function
        )

    else:

        vectorstore = FAISS.from_documents(
            all_docs,
            embedding_function
        )

    vectorstore.save_local(
        FAISS_PATH
    )

    db.close()