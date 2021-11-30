"""
Contains the path operations of URL shortener API.
"""
import random
import string
from urllib.parse import urljoin

from fastapi import APIRouter, HTTPException

from app.models import Url as UrlModel
from app.schemas import Url as UrlIn

router = APIRouter()


@router.post("/")
async def shorten_url(url: UrlIn):
    """
    Receive a URL and an optional custom_name from request body and return the original URL and a shortened URL.
    :param url: Request body that consists of a URL and an optional custom name
    :return: The original URL and a shortened URL
    """
    if url.custom_name:
        short_name = url.custom_name
    else:
        # Generate a random short name
        short_name = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                             for _ in range(int(os.environ["RNG_LENGTH"])))

    # Query if name is already in database
    # The length is 0 if it doesn't exist
    name_exist = UrlModel.objects(short_name=short_name)
    if len(name_exist) > 0:
        raise HTTPException(status_code=400, detail=f"Invalid custom name: {short_name} is in use")

    short_url = urljoin(os.environ["BASE_URL"], short_name)

    # Save the url to database
    good_url = UrlModel(url=url.url, short_name=short_name, short_url=short_url)
    good_url.save()

    return {"url": url.url,
            "short_url": short_url}
