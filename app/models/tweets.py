import typing as t

from pydantic import BaseModel


class Tweet(BaseModel):
    url: str
    image: t.Optional[str] = None
    image_width: t.Optional[str] = None
    image_height: t.Optional[str] = None
    title: str
    description: str
    video: t.Optional[str] = None
    video_secure_url: t.Optional[str] = None
    video_height: t.Optional[str] = None
    video_width: t.Optional[str] = None
    video_type: t.Optional[str] = None