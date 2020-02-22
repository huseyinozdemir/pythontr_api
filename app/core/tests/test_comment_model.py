from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Category, Article, Comment

def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)

def test_category(name='Php Programlama', short_name='php'):
    return Category.objects.create(
        user=test_user(),
        name=name,
        short_name=short_name,
    )


class ModelTests(TestCase):

    def test_comment_str(self):
        category = test_category()
        user = test_user()
        article = Article.objects.create(
            user=user,
            title='Sqrt fonksiyonu  pythontr.com',
            description='bla bla....',
        )
        article.categories.add(category)

        comment = Comment.objects.create(
            article_id=article.id,
            comment_id=0,
            email='huseyin@pythontr.com',
        )

        self.assertEqual(str(comment), comment.title)

    def test_reply_comment(self):
        category = test_category()
        user = test_user()
        article = Article.objects.create(
            user=user,
            title='Sqrt fonksiyonu  pythontr.com',
            description='bla bla....',
        )
        article.categories.add(category)

        comment = Comment.objects.create(
            article_id=article.id,
            comment_id=0,
            content='It is wonderful content',
            email='huseyin@pythontr.com',
        )

        comment_reply = Comment.objects.create(
            article_id=article.id,
            comment_id=comment.id,
            content='I am not thinking.....',
            email='huseyin@pythontr.com',
        )

        self.assertGreaterEqual(comment_reply.comment_id, 0)
