from ninja import Router
from ninja_jwt.authentication import JWTAuth
from .models import Article, Comment
from .serializers import (
    ArticleSchema, ArticleCreateSchema, ArticleUpdateSchema,
    CommentSchema, CommentCreateSchema, CommentUpdateSchema
)
from typing import List

router = Router()
jwt_auth = JWTAuth()


@router.post("/articles", response=ArticleSchema, auth=jwt_auth)
def create_article(request, data: ArticleCreateSchema):
    article = Article.objects.create(author=request.auth, **data.dict())
    return article

@router.get("/articles", response=List[ArticleSchema])
def list_articles(request):
    return Article.objects.all()

@router.get("/articles/{article_id}", response=ArticleSchema)
def get_article(request, article_id: int):
    return Article.objects.get(id=article_id)

@router.put("/articles/{article_id}", response=ArticleSchema, auth=jwt_auth)
def update_article(request, article_id: int, data: ArticleUpdateSchema):
    article = Article.objects.get(id=article_id)
    if article.author != request.auth:
        return 403, {"detail": "You can edit only your own articles"}
    for field, value in data.dict(exclude_unset=True).items():
        setattr(article, field, value)
    article.save()
    return article

@router.delete("/articles/{article_id}", auth=jwt_auth)
def delete_article(request, article_id: int):
    article = Article.objects.get(id=article_id)
    if article.author != request.auth:
        return 403, {"detail": "You can delete only your own articles"}
    article.delete()
    return {"detail": "Article deleted"}


@router.post("/comments", response=CommentSchema, auth=jwt_auth)
def create_comment(request, data: CommentCreateSchema):
    article = Article.objects.get(id=data.article_id)
    comment = Comment.objects.create(author=request.auth, article=article, content=data.content)
    return comment

@router.get("/comments/{article_id}", response=List[CommentSchema])
def list_comments(request, article_id: int):
    return Comment.objects.filter(article_id=article_id)

@router.put("/comments/{comment_id}", response=CommentSchema, auth=jwt_auth)
def update_comment(request, comment_id: int, data: CommentUpdateSchema):
    comment = Comment.objects.get(id=comment_id)
    if comment.author != request.auth:
        return 403, {"detail": "You can edit only your own comments"}
    for field, value in data.dict(exclude_unset=True).items():
        setattr(comment, field, value)
    comment.save()
    return comment

@router.delete("/comments/{comment_id}", auth=jwt_auth)
def delete_comment(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    if comment.author != request.auth:
        return 403, {"detail": "You can delete only your own comments"}
    comment.delete()
    return {"detail": "Comment deleted"}
