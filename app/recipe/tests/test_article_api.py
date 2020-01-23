from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

# from recipe.serializers import ArticleSerializer


ARTICLES_URL = reverse('recipe:article-list')
ARTICLES_DETAIL_URL = reverse('recipe:article-detail', kwargs={'pk': '1'})


class PublicArticleApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test1@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()

    def test_list_login_not_requried(self):
        res = self.client.get(ARTICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_404_article_login_not_required(self):
        res = self.client.get(ARTICLES_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_article(self):
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
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
