from ninja import Schema
from typing import Optional
from datetime import datetime

class ArticleCreateSchema(Schema):
    title: str
    content: str

class ArticleUpdateSchema(Schema):
    title: Optional[str]
    content: Optional[str]

class ArticleSchema(Schema):
    id: int
    author_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class CommentCreateSchema(Schema):
    article_id: int
    content: str

class CommentUpdateSchema(Schema):
    content: Optional[str]

class CommentSchema(Schema):
    id: int
    article_id: int
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime
