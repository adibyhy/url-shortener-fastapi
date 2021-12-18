"""
Contains the path operations for the home page.
"""
from datetime import datetime

import fastapi
import pydantic.error_wrappers
from fastapi import Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.models import Url as UrlModel
from app.routers.urls import shorten_url
from app.schemas import Url as UrlIn

templates = Jinja2Templates("app/templates")

router = fastapi.APIRouter()


@router.get('/', include_in_schema=False)
def index(request: Request):
    """
    Display the home page.
    :param request:
    :return: Home page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.post('/')
async def form_submit_url(request: Request, url: str = Form(...), custom_name: str = Form(None)):
    """
    Receive a URL and an optional custom_name from form-data and return a shortened URL.
    :param request:
    :param url: Long URL to be shortened
    :param custom_name: User-provided name, optional
    :return: Shortened URL
    """
    try:
        data = UrlIn(url=url, custom_name=custom_name)
    except pydantic.error_wrappers.ValidationError:
        return templates.TemplateResponse("400.html", status_code=400,
                                          context={'request': request, 'result': f"{url} is not a valid URL"})
    try:
        resp = await shorten_url(data)
    except HTTPException as e:
        return templates.TemplateResponse("400.html", status_code=400,
                                          context={'request': request, 'result': e.detail})
    return templates.TemplateResponse("index.html", context={'request': request, 'result': resp['short_url']})


@router.get("/{short_name}")
async def redirect_url(short_name: str):
    """
    Query the database for a matching short name and redirect the browser to the original URL.
    :param short_name: The short identifier for the long URL
    :return: Redirect response
    """
    url = UrlModel.objects(short_name=short_name)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.update_one(upsert=True, inc__use_count=1)
    url.update_one(upsert=True, set__last_accessed=datetime.utcnow())
    url = url[0].to_mongo().to_dict()
    response = RedirectResponse(url=url['url'])
    return response
