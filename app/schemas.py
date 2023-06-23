from pydantic import BaseModel


class Post(BaseModel):
    p_title: str
    p_content: str
    published: bool = True
