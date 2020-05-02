from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core.models import Category, Article


def test_user(email='testarticle@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


def test_user_other(email='testarticleother@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


def test_category(name='Python Article Programlama',
                  title='Python Öğren',
                  short_name='python article'):
    return Category.objects.create(
        user=test_user(),
        name=name,
        short_name=short_name,
    )


class ModelTests(TestCase):

    def test_article_str(self):
        category = test_category()
        user = test_user_other()
        article = Article.objects.create(
            user=user,
            title='Python programlama',
            description='python',
            approval_user=user,
        )
        article.categories.add(category)

        self.assertEqual(str(article), article.title)

    def test_article_title_uniqe_check(self):
        Article.objects.create(
            user=test_user(),
            title='Python',
            description='python',
            approval_user=test_user_other(),
        )
        with self.assertRaises(IntegrityError):
            Article.objects.create(
                user=test_user(),
                title='Python',
                description='python2',
                approval_user=test_user_other(),
            )

    def test_article_category_type_error(self):
        with self.assertRaises(TypeError):
            Article.objects.create(
                user=test_user_other(),
                category=None,
                title='Python',
                description='python',
                approval_user=test_user(),
            )
