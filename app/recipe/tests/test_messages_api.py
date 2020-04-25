from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Message


MESSAGES_URL = reverse('recipe:message-list')
MESSAGES_INBOX_URL = '{}{}'.format(MESSAGES_URL, '?inbox=true')
MESSAGES_OUTBOX_URL = '{}{}'.format(MESSAGES_URL, '?outbox=true')


def detail_url(id=1):
    return reverse('recipe:message-detail', args=[id])


class PublicMessageApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test1@hotmail.com',
                '123qwe'
        )
        self.sender = get_user_model().objects.create_user(
                'test2@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()

    def test_list_message_login_requried(self):
        res = self.client.get(MESSAGES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dont_create_message(self):
        message = {
            'sender': [self.sender.id],
            'user': [self.user.id],
            'subjet': 'This is a test',
            'content': 'Hello, How are you!',
            'ip': '127.0.0.1'
        }
        res = self.client.post(MESSAGES_URL, message)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMessageApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                'test12@hotmail.com',
                '123qwe'
        )
        self.sender = get_user_model().objects.create_user(
                'test13@hotmail.com',
                '123qwe'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_message(self):
        message = {
            'sender': [self.sender.id],
            'user': [self.user.id],
            'subject': 'This is a test',
            'content': 'Hello, How are you!',
            'ip': '127.0.0.1'
        }

        res = self.client.post(MESSAGES_URL, message)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_dont_delete_message(self):
        message = Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello,',
            content='How are you!',
            ip='127.0.0.1',
        )

        url = detail_url(message.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_all_messages(self):
        Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello,',
            content='How are you!',
            ip='127.0.0.1',
        )

        Message.objects.create(
            sender=self.user,
            user=self.sender,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
        )

        other_sender = get_user_model().objects.create_user(
                'test222@hotmail.com',
                '123qwe'
        )

        other_user = get_user_model().objects.create_user(
                'test223@hotmail.com',
                '123qwe'
        )

        Message.objects.create(
            sender=other_sender,
            user=other_user,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
        )

        res = self.client.get(MESSAGES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_inbox_messages(self):
        Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello,',
            content='How are you!',
            ip='127.0.0.1',
        )

        Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
            is_delete=True,
        )

        other_sender = get_user_model().objects.create_user(
                'test222@hotmail.com',
                '123qwe'
        )

        other_user = get_user_model().objects.create_user(
                'test223@hotmail.com',
                '123qwe'
        )

        Message.objects.create(
            sender=other_sender,
            user=other_user,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
        )

        res = self.client.get(MESSAGES_INBOX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_get_outbox_messages(self):
        Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello,',
            content='How are you!',
            ip='127.0.0.1',
        )

        Message.objects.create(
            sender=self.user,
            user=self.sender,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
        )

        other_user = get_user_model().objects.create_user(
                'test223@hotmail.com',
                '123qwe'
        )

        Message.objects.create(
            sender=self.user,
            user=other_user,
            subject='re:Hello,',
            content='Thank you and you!',
            ip='127.0.0.1',
        )

        res = self.client.get(MESSAGES_OUTBOX_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_single_messages(self):
        Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello,',
            content='How are you!',
            ip='127.0.0.1',
        )
        message = Message.objects.create(
            sender=self.sender,
            user=self.user,
            subject='Hello 2,',
            content='How are you!',
            ip='127.0.0.1',
        )
        url = detail_url(message.id)

        res = self.client.get(url)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
