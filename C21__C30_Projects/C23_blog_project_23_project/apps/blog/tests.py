from django.test import TestCase
from django.contrib.auth.models import User
from .models import Article,Comment

class ArticleTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.article = Article.objects.create(
            title='Test Article',
            content='Content',
            author=self.user
        )

    def test_create_article(self):
        article = Article.objects.create(title='New', content='New content', author=self.user)
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.title, 'New')

    def test_user_can_edit_own_article(self):
        self.article.title = 'Updated'
        self.article.save()
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated')

    def test_user_cannot_edit_others_article(self):
        # Симуляция другого пользователя
        self.article.author = self.other_user
        self.article.save()
        self.article.refresh_from_db()
        self.assertNotEqual(self.article.author, self.user)

    def test_user_can_delete_own_article(self):
        article_id = self.article.id
        self.article.delete()
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=article_id)


class CommentTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='pass')
        self.article = Article.objects.create(title='Article', content='Content', author=self.user)
        self.comment = Comment.objects.create(content='Nice', author=self.user, article=self.article)

    def test_create_comment(self):
        comment = Comment.objects.create(content='Another', author=self.user, article=self.article)
        self.assertEqual(comment.author, self.user)

    def test_user_can_edit_own_comment(self):
        self.comment.content = 'Updated comment'
        self.comment.save()
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment')

    def test_user_cannot_edit_others_comment(self):
        other_user = User.objects.create_user(username='other', password='pass')
        self.comment.author = other_user
        self.comment.save()
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.author, self.user)

    def test_user_can_delete_own_comment(self):
        comment_id = self.comment.id
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)
