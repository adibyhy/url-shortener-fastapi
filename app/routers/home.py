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
    return templates.TemplateResponse("index.html", {"request": request})


@router.post('/')
async def form_submit_url(request: Request, url: str = Form(...), custom_name: str = Form(None)):
    try:
        data = UrlIn(url=url, custom_name=custom_name)
    except pydantic.error_wrappers.ValidationError:
        return templates.TemplateResponse("400.html",
                                          context={'request': request, 'result': f"{url} is not a valid URL"})
    resp = await shorten_url(data)
    return templates.TemplateResponse("index.html", context={'request': request, 'result': resp['short_url']})


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
