from config import settings

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from pydantic import BaseModel
from typing import Optional

class Base(DeclarativeBase): pass

class Crimes(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(String, nullable=False)
    coordinates = Column(String, nullable=False)
    address = Column(String, nullable=False)
    article = Column(String, nullable=False)
    article_name = Column(String, nullable=True)
    count = Column(Integer, nullable=False)
    icon_id = Column(Integer, nullable=True)

engine = create_engine(settings.database_url)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def index():
    return FileResponse("public/index.html")

@app.get("/api/data")
def get_list():
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()

    crimes = db.query(Crimes).all()
    db.close()
    
    return crimes

app.mount("/", StaticFiles(directory="public"))