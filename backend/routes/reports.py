from fastapi import APIRouter
from fastapi import Header
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse

from database.db import SessionLocal
from database.models import Report
from database.user_model import User

from auth.auth import verify_token

from services.vector_service import rebuild_vectorstore

import os

router = APIRouter()


def get_current_user(authorization: str):

    db = SessionLocal()

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if not payload:

        db.close()

        return None

    email = payload["sub"]

    user = db.query(User).filter(
        User.email == email
    ).first()

    db.close()

    return user


# GET CURRENT USER REPORTS
@router.get("/reports")
def get_reports(

    authorization: str = Header(...)

):

    user = get_current_user(
        authorization
    )

    if not user:

        return []

    db = SessionLocal()

    reports = db.query(Report).filter(
        Report.user_id == user.id
    ).all()

    db.close()

    return reports

# DOWNLOAD REPORT
@router.get("/download/{report_id}")
def download_report(

    report_id: int,

    authorization: str = Header(...)

):

    user = get_current_user(
        authorization
    )

    print(
        "DOWNLOAD USER:",
        user.email if user else None
    )

    if not user:

        return {
            "message":
            "Unauthorized"
        }

    db = SessionLocal()

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:

        db.close()

        return {
            "message":
            "Report not found"
        }

    print(
        "REPORT OWNER ID:",
        report.user_id
    )

    print(
        "CURRENT USER ID:",
        user.id
    )

    if report.user_id != user.id:

        db.close()

        return {
            "message":
            "Access denied"
        }

    db.close()

    return FileResponse(
        path=report.filepath,
        filename=report.filename,
        media_type="application/pdf"
    )


# DELETE REPORT
@router.delete("/delete/{report_id}")
def delete_report(

    report_id: int,

    authorization: str = Header(...),

    background_tasks: BackgroundTasks = BackgroundTasks()

):

    user = get_current_user(
        authorization
    )

    print(
        "DELETE USER:",
        user.email if user else None
    )

    if not user:

        return {
            "message":
            "Unauthorized"
        }

    db = SessionLocal()

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:

        db.close()

        return {
            "message":
            "Report not found"
        }

    print(
        "REPORT OWNER ID:",
        report.user_id
    )

    print(
        "CURRENT USER ID:",
        user.id
    )

    if report.user_id != user.id:

        db.close()

        return {
            "message":
            "Access denied"
        }

    if os.path.exists(
        report.filepath
    ):

        os.remove(
            report.filepath
        )

    db.delete(report)

    db.commit()

    background_tasks.add_task(
        rebuild_vectorstore
    )

    db.close()

    return {
        "message":
        "Report deleted"
    }