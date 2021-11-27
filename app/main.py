import os

from fastapi import FastAPI
from mongoengine import connect

from app.routers import urls, home


def create_app():
    instance = FastAPI(title="URL Shortener")
    instance.include_router(home.router)
    instance.include_router(urls.router)
    return instance


app = create_app()


@app.on_event("startup")
async def mongodb_connect():
    connect(host=os.environ["MONGODB_URI"])
