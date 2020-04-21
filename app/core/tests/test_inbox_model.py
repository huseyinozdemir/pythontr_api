from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Q

from core.models import Inbox


def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_inbox_str(self):
        user = test_user('user@hotmail.com')
        sender = test_user('sender@hotmail.com')
        inbox = Inbox.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I want to meet you! Plase.',
            ip='127.0.0.1',
        )

        self.assertEqual(str(inbox), inbox.subject)

    def test_inbox_delete(self):
        user = test_user('user@hotmail.com')
        sender = test_user('sender@hotmail.com')
        inbox = Inbox.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I want to meet you! Plase.',
            ip='127.0.0.1',
        )

        inbox.is_delete = 1
        inbox.save()

        filter_inbox = Inbox.objects.filter(id=inbox.id).last()
        self.assertEqual(filter_inbox, None)

        inbox.is_delete = 0
        inbox.save()

        filter_second_inbox = Inbox.objects.filter(id=inbox.id).last()
        self.assertEqual(filter_second_inbox.is_delete, 0)

    def test_get_reciver_user_inbox(self):
        user = test_user('getlist@gmail.com')
        sender = test_user('test@msn.com')
        Inbox.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I wanna ask a question about your apache content',
            ip='127.0.0.1',
        )
        Inbox.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='Of course, what is the problem, how can I help you?',
            ip='127.0.0.1',
        )
        Inbox.objects.create(
            sender=sender,
            user=user,
            subject='Re:Hello',
            content='Thank you for your answer bla.. bla..',
            ip='127.0.0.1',
        )
        Inbox.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='....sure...',
            ip='127.0.0.1',
        )

        inboxes = Inbox.objects.filter(
            Q(user=user) | Q(sender=user)
        ).order_by('id')
        self.assertEqual(inboxes.count(), 4)
