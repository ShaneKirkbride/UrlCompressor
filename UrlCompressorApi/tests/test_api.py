import importlib
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_ROOT, ".."))
sys.path.insert(0, PROJECT_ROOT)

import UrlCompressorApi.database as db
from UrlCompressorApi.models import Base


def create_test_app():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db.engine = engine
    db.SessionLocal = TestingSessionLocal
    import UrlCompressorApi.UrlCompressorApi as api
    importlib.reload(api)
    return api.app


def test_shorten_and_redirect(tmp_path):
    app = create_test_app()
    client = TestClient(app)
    response = client.post("/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 200
    short_url = response.json()["short_url"]
    code = short_url.rsplit("/", 1)[-1]
    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"].rstrip('/') == "https://example.com"
