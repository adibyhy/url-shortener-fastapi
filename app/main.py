"""
Contains the main application initialization.
"""
import os

from fastapi import FastAPI
from mongoengine import connect

from app.routers import urls, home


def create_app():
    """
    Create FastAPI instance and its routers.
    :return: FastAPI application instance
    """
    instance = FastAPI(title="URL Shortener")
    instance.include_router(home.router)
    instance.include_router(urls.router, prefix="/api/shorten")
    return instance


app = create_app()


@app.on_event("startup")
async def mongodb_connect():
    """Connect to MongoDB using connection string at server startup."""
    connect(host=os.environ["MONGODB_URI"])
