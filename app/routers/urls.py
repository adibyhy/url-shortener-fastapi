import os
import random
import string
from datetime import datetime
from urllib.parse import urljoin

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse

from app.models import Url as UrlModel
from app.schemas import Url as UrlIn

router = APIRouter()


@router.post("/")
async def shorten_url(url: UrlIn):
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


@router.get("/{short_name}")
async def redirect_url(short_name: str):
    # Query the database for the document that matches the short_code from the path param
    url = UrlModel.objects(short_name=short_name)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.update_one(upsert=True, inc__use_count=1)
    url.update_one(upsert=True, set__last_accessed=datetime.utcnow())
    url = url[0].to_mongo().to_dict()
    response = RedirectResponse(url=url['url'])
    return response
