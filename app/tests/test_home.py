import random
import string

from app.tests.test_main import client


def test_read_home():
    response = client.get("/")
    assert response.status_code == 200


def test_form_submit_url():
    url_00 = {"url": "duckduckgo.com"}
    url_01 = {"url": "http://duckduckgo.com"}
    url_02 = {"url": "http://duckduckgo.com",
              "custom_name": "ddg"}
    url_03 = {"url": "http://duckduckgo.com",
              "custom_name": ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                     for _ in range(5))}
    url_04 = {"url": "duckduckgo"}

    response = client.post("/", data=url_00)
    assert response.status_code == 200

    response = client.post("/", data=url_01)
    assert response.status_code == 200

    # This may fail on the first run because database isn't populated yet
    response = client.post("/", data=url_02)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid custom name: ddg is in use"}

    response = client.post("/", data=url_03)
    assert response.status_code == 200

    response = client.post("/", data=url_04)
    assert "duckduckgo is not a valid URL" in response.text


def test_redirect_url():
    response = client.get("/ddg")
    assert response.status_code == 200

    response = client.get("/thisdoesnotexist")
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}
