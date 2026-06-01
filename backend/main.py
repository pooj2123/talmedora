from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router
from routes.chat import router as chat_router

from database.db import engine
from database.models import Base
from routes.reports import router as reports_router

from database.user_model import User
from routes.auth import router as auth_router




app = FastAPI()
app.include_router(reports_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "AI Report Assistant Running"}