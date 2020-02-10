from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, Article

# from recipe.serializers import ArticleSerializer


ARTICLES_URL = reverse('recipe:article-list')


def detail_url(id=1):
    return reverse('recipe:article-detail', args=[id])


class PublicArticleApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test1@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_not_login_requried(self):
        res = self.client.get(ARTICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_404_article_login_not_required(self):
        url = detail_url()
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_dont_create_article(self):
        self.client.force_authenticate(self.user)
        category = Category.objects.create(
            user=self.user, name="veritabani mysql", short_name='mysql'
        )
        content = {
            'categories': [category.id],
            'title': 'How to update for dictionary',
            'title_h1': 'Upade for dictionary on Python Programming Language',
            'description': 'Bla bla bla',
            'content': '............... bla bla ...  bla ........',
            'user': [self.user.id]
        }
        res = self.client.post(ARTICLES_URL, content)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # res = get_article(self.client, res.data['id'])
        # self.assertEquals(res.status_code, status.HTTP_200_OK)


class PrivateArticleApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test12@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_update_article(self):
        self.is_staff = True
        category = Category.objects.create(
            user=self.user, name="veritabani mysql", short_name='mysql'
        )
        article = Article.objects.create(
            title='How to update for dictionary',
            title_h1='Upade for dictionary on Python Programming Language',
            description='Bla bla bla',
            content='............... bla bla ...  bla ........',
            is_active=True,
            user=self.user
        )
        content = {
            'id': article.id,
            'categories': [category.id],
            'title': 'Deneme',
            'title_h1': 'Upade for dictionary on Python Programming Language',
            'description': 'Bla bla bla',
            'content': '............... bla bla ...  bla ........',
            'user': [self.user.id]
        }
        url = detail_url(article.id)

        res = self.client.put(url, content)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data['title'], content['title'])
