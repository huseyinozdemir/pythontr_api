from django.urls import reverse
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article
from core.models import Comment
from django.contrib.auth import get_user_model

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

class PrivateCommentApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test12@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_create_comment(self):
        self.is_staff = True
        article = Article.objects.create(
            title='Pythont.Com on BBC',
            title_h1='Do you hear us? Pythontr...',
            description='bla bla....',
            content='bla bla....bla......',
            is_active=True,
        )

        content = {
            "content": "Deneme",
            "email": "test12@hotmail.com",
            "name": "TEST",
            "ip": "127.0.0.1",
            "user": [self.user.id],
            "content_type": ContentType.objects.get_for_model(Article).id,
            "object_id": article.id,
            "comments": [],
        }
        res = self.client.post(COMMENT_URL, content)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        
    def test_update_article_comment(self):
        self.is_staff = True

        article = Article.objects.create(
            title='Pythont.Com on BBC',
            title_h1='Do you hear us? Pythontr...',
            description='bla bla....',
            content='bla bla....bla......',
            is_active=True,
        )
        comment = Comment.objects.create(
            content='Test Comment',
            email='test12@hotmail.com',
            name='TEST',
            ip='127.0.0.1',
            content_type=ContentType.objects.get_for_model(Article),
            object_id= article.id,
            is_active=True,
            user=self.user
        )
        content = {
            'content': '............... bla bla ...  bla ........',          
        }

        url = COMMENT_URL + str(comment.id) + '/?comment_type=article' # commentin commentini update etmek için comment_type=comment &parent_id=<geçerli_parent_id> parentı varsa
 
        res = self.client.patch(url, content)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data['content'], content['content'])

    def test_update_comment_comment(self):
        self.is_staff = True

        article = Article.objects.create(
            title='Pythont.Com on BBC',
            title_h1='Do you hear us? Pythontr...',
            description='bla bla....',
            content='bla bla....bla......',
            is_active=True,
        )
        parent_comment = Comment.objects.create(
            content='Test Comment Parent',
            email='test12@hotmail.com',
            name='TEST Parent',
            ip='127.0.0.1',
            content_type=ContentType.objects.get_for_model(Article),
            object_id= article.id,
            is_active=True,
            user=self.user
        )

        child_comment = Comment.objects.create(
            content='Test Comment Child',
            email='test12@hotmail.com',
            name='TEST Child',
            ip='127.0.0.1',
            content_type=ContentType.objects.get_for_model(Comment),
            object_id= parent_comment.id,
            is_active=True,
            user=self.user
        )
        content = {
            'content': '............... bla bla ...  bla ........',          
        }

        url = COMMENT_URL + str(child_comment.id) + '/?comment_type=comment' # commentin commentini update etmek için comment_type=comment &parent_id=<geçerli_parent_id> parentı varsa
 
        res = self.client.patch(url, content)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data['content'], content['content'])