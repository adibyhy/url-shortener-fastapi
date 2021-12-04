import random
import string

from app.tests.test_main import client


def test_shorten_url():
    url_00 = {"url": "duckduckgo.com"}
    url_01 = {"url": "http://duckduckgo.com"}
    url_02 = {"url": "http://duckduckgo.com",
              "custom_name": "ddg"}
    url_03 = {"url": "http://duckduckgo.com",
              "custom_name": ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                                     for _ in range(5))}
    url_04 = {"url": "duckduckgo"}

    response = client.post("/api/shorten/", json=url_00)
    short_url_00 = response.json()["short_url"]
    assert response.status_code == 200

    response = client.post("/api/shorten/", json=url_01)
    short_url_01 = response.json()["short_url"]
    assert response.status_code == 200

    # Both short urls should be equal because they're pointing to the same url
    assert short_url_00 == short_url_01

    # This may fail on the first run because database isn't populated yet
    response = client.post("/api/shorten/", json=url_02)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid custom name: ddg is in use"}

    response = client.post("/api/shorten/", json=url_03)
    assert response.status_code == 200

    response = client.post("/api/shorten/", json=url_04)
    assert response.status_code == 422
