"""
Contains pydantic schemas.
"""

from typing import Optional

import validators
from pydantic import BaseModel, validator


class Url(BaseModel):
    url: str
    custom_name: Optional[str] = None

    @validator("url")
    def url_must_be_correct(cls, v):
        schemas = ["http://",
                   "https://"]
        if not validators.url(v):
            for schema in schemas:
                t = schema + v
                if validators.url(t):
                    v = t
                    return v
            raise ValueError("Invalid URL")
        return v
