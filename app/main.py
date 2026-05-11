import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import engine
from app.routers import todos
from app.services import s3_service

load_dotenv()

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    s3_service.create_bucket_if_not_exists()
    yield


app = FastAPI(
    title=os.getenv("APP_NAME", "TODO App"),
    description="A TODO app using FastAPI, PostgreSQL, and LocalStack-backed S3/SES",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(todos.router)


@app.get("/")
def root():
    return {
        "message": "TODO App API is running with LocalStack.",
        "docs": "/docs",
        "frontend": "/static/index.html",
    }
