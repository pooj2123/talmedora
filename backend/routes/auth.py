from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from database.db import SessionLocal
from database.user_model import User

from auth.security import (
    hash_password,
    verify_password
)

from auth.auth import (
    create_access_token,
    verify_token,
    oauth2_scheme
)

router = APIRouter()


class RegisterRequest(BaseModel):

    email: str

    password: str


class LoginRequest(BaseModel):

    email: str

    password: str


@router.post("/register")
def register(request: RegisterRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:

        db.close()

        return {
            "message": "User already exists"
        }

    user = User(

        email=request.email,

        password=hash_password(
            request.password
        )
    )

    db.add(user)

    db.commit()

    db.close()

    return {

        "message":
        "Registration successful"
    }


@router.post("/login")
def login(request: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
    request.password,
    user.password
):

        db.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({

        "sub": user.email
    })

    db.close()

    return {

        "access_token": token,

        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    token: str = Depends(
        oauth2_scheme
    )
):

    payload = verify_token(token)

    if not payload:

        return {
            "message":
            "Invalid token"
        }

    return {

        "user":
        payload["sub"]
    }