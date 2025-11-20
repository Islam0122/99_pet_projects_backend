from ninja import Router
from ninja_jwt.authentication import JWTAuth
from .models import Article, Comment
from .serializers import (
    ArticleSchema, ArticleCreateSchema, ArticleUpdateSchema,
    CommentSchema, CommentCreateSchema, CommentUpdateSchema
)
from typing import List
import logging

router = Router()
jwt_auth = JWTAuth()
logger = logging.getLogger(__name__)


@router.post("/articles", response=ArticleSchema, auth=jwt_auth)
def create_article(request, data: ArticleCreateSchema):
    try:
        article = Article.objects.create(author=request.auth, **data.dict())
        logger.info(f"Article created: id={article.id}, author={request.auth.username}, title='{article.title}'")
        return article
    except Exception as e:
        logger.error(f"Error creating article: {e}, user={request.auth.username}")
        raise


@router.get("/articles", response=List[ArticleSchema])
def list_articles(request):
    try:
        articles = Article.objects.all()
        logger.info(f"Articles listed: count={articles.count()}")
        return articles
    except Exception as e:
        logger.error(f"Error listing articles: {e}")
        raise


@router.get("/articles/{article_id}", response=ArticleSchema)
def get_article(request, article_id: int):
    try:
        article = Article.objects.get(id=article_id)
        logger.info(f"Article viewed: id={article_id}, title='{article.title}'")
        return article
    except Article.DoesNotExist:
        logger.warning(f"Article not found: id={article_id}")
        raise
    except Exception as e:
        logger.error(f"Error getting article: {e}, id={article_id}")
        raise


@router.put("/articles/{article_id}", response=ArticleSchema, auth=jwt_auth)
def update_article(request, article_id: int, data: ArticleUpdateSchema):
    try:
        article = Article.objects.get(id=article_id)
        if article.author != request.auth:
            logger.warning(f"Unauthorized article edit attempt: article_id={article_id}, user={request.auth.username}")
            return 403, {"detail": "You can edit only your own articles"}

        for field, value in data.dict(exclude_unset=True).items():
            setattr(article, field, value)
        article.save()
        logger.info(f"Article updated: id={article_id}, user={request.auth.username}")
        return article
    except Article.DoesNotExist:
        logger.warning(f"Article not found for update: id={article_id}")
        raise
    except Exception as e:
        logger.error(f"Error updating article: {e}, id={article_id}, user={request.auth.username}")
        raise


@router.delete("/articles/{article_id}", auth=jwt_auth)
def delete_article(request, article_id: int):
    try:
        article = Article.objects.get(id=article_id)
        if article.author != request.auth:
            logger.warning(
                f"Unauthorized article delete attempt: article_id={article_id}, user={request.auth.username}")
            return 403, {"detail": "You can delete only your own articles"}

        article.delete()
        logger.info(f"Article deleted: id={article_id}, user={request.auth.username}")
        return {"detail": "Article deleted"}
    except Article.DoesNotExist:
        logger.warning(f"Article not found for deletion: id={article_id}")
        raise
    except Exception as e:
        logger.error(f"Error deleting article: {e}, id={article_id}, user={request.auth.username}")
        raise


@router.post("/comments", response=CommentSchema, auth=jwt_auth)
def create_comment(request, data: CommentCreateSchema):
    try:
        article = Article.objects.get(id=data.article_id)
        comment = Comment.objects.create(author=request.auth, article=article, content=data.content)
        logger.info(f"Comment created: id={comment.id}, article_id={article.id}, author={request.auth.username}")
        return comment
    except Article.DoesNotExist:
        logger.warning(f"Article not found for comment: article_id={data.article_id}")
        raise
    except Exception as e:
        logger.error(f"Error creating comment: {e}, user={request.auth.username}")
        raise


@router.get("/comments/{article_id}", response=List[CommentSchema])
def list_comments(request, article_id: int):
    try:
        comments = Comment.objects.filter(article_id=article_id)
        logger.info(f"Comments listed for article: article_id={article_id}, count={comments.count()}")
        return comments
    except Exception as e:
        logger.error(f"Error listing comments: {e}, article_id={article_id}")
        raise


@router.put("/comments/{comment_id}", response=CommentSchema, auth=jwt_auth)
def update_comment(request, comment_id: int, data: CommentUpdateSchema):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.author != request.auth:
            logger.warning(f"Unauthorized comment edit attempt: comment_id={comment_id}, user={request.auth.username}")
            return 403, {"detail": "You can edit only your own comments"}

        for field, value in data.dict(exclude_unset=True).items():
            setattr(comment, field, value)
        comment.save()
        logger.info(f"Comment updated: id={comment_id}, user={request.auth.username}")
        return comment
    except Comment.DoesNotExist:
        logger.warning(f"Comment not found for update: id={comment_id}")
        raise
    except Exception as e:
        logger.error(f"Error updating comment: {e}, id={comment_id}, user={request.auth.username}")
        raise


@router.delete("/comments/{comment_id}", auth=jwt_auth)
def delete_comment(request, comment_id: int):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.author != request.auth:
            logger.warning(
                f"Unauthorized comment delete attempt: comment_id={comment_id}, user={request.auth.username}")
            return 403, {"detail": "You can delete only your own comments"}

        comment.delete()
        logger.info(f"Comment deleted: id={comment_id}, user={request.auth.username}")
        return {"detail": "Comment deleted"}
    except Comment.DoesNotExist:
        logger.warning(f"Comment not found for deletion: id={comment_id}")
        raise
    except Exception as e:
        logger.error(f"Error deleting comment: {e}, id={comment_id}, user={request.auth.username}")
        raise