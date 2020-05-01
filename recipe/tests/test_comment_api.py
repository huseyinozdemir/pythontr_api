from django.urls import reverse
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article


COMMENT_URL = reverse('recipe:comment-list')


class PublicCommentApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_comment_list(self):
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_create(self):
        article = Article.objects.create(
            title='Pythont.Com on BBC',
            title_h1='Do you hear us? Pythontr...',
            description='bla bla....',
            content='bla bla....bla......',
            is_active=True,
        )
        content_type = ContentType.objects.get_for_model(Article)
        content = {
            'content_type': content_type.id,
            'object_id': article.id,
            'email': 'tttes@gmail.com',
            'name': 'Ttte',
            'ip': '127.0.0.1',
            'is_active': True,
        }
        res = self.client.post(COMMENT_URL, content)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
