import os

from fastapi.testclient import TestClient
from mongoengine import connect

from app.main import app

client = TestClient(app)
connect(host=os.environ["MONGODB_URI_TESTS"])
