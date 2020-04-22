from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Q

from core.models import Message


def test_user(email='test@hotmail.com', password='123qwe'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_message_str(self):
        user = test_user('user@hotmail.com')
        sender = test_user('sender@hotmail.com')
        message = Message.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I want to meet you! Plase.',
            ip='127.0.0.1',
        )

        self.assertEqual(str(message), message.subject)

    def test_message_delete(self):
        user = test_user('user@hotmail.com')
        sender = test_user('sender@hotmail.com')
        message = Message.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I want to meet you! Plase.',
            ip='127.0.0.1',
        )

        message.is_delete = True
        message.save()

        filter_message = Message.objects.filter(id=message.id).last()
        self.assertEqual(filter_message, None)

        message.is_delete = False
        message.save()

        filter_second_message = Message.objects.filter(id=message.id).last()
        self.assertEqual(filter_second_message.is_delete, False)

    def test_get_user_inbox_and_autbox(self):
        user = test_user('getlist@gmail.com')
        sender = test_user('test@msn.com')
        Message.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I wanna ask a question about your apache content',
            ip='127.0.0.1',
        )
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='Of course, what is the problem, how can I help you?',
            ip='127.0.0.1',
        )
        Message.objects.create(
            sender=sender,
            user=user,
            subject='Re:Hello',
            content='Thank you for your answer bla.. bla..',
            ip='127.0.0.1',
        )
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='....sure...',
            ip='127.0.0.1',
        )

        messages = Message.objects.filter(
            Q(user=user) | Q(sender=user)
        ).order_by('id')
        self.assertEqual(messages.count(), 4)

    def test_get_user_inbox(self):
        user = test_user('getlistin@gmail.com')
        sender = test_user('testin@msn.com')
        Message.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I wanna ask a question about your apache content',
            ip='127.0.0.1',
        )
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='Of course, what is the problem, how can I help you?',
            ip='127.0.0.1',
        )
        sender_message = Message.objects.create(
            sender=sender,
            user=user,
            subject='Re:Hello',
            content='Thank you for your answer bla.. bla..',
            ip='127.0.0.1',
        )
        sender_message.is_delete = True
        sender_message.save()
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='....sure...',
            ip='127.0.0.1',
        )
        messages = Message.objects.inbox(user=user).order_by('id')
        self.assertEqual(messages.count(), 1)

    def test_get_user_outbox(self):
        user = test_user('getlistout@gmail.com')
        sender = test_user('testout@msn.com')
        Message.objects.create(
            sender=sender,
            user=user,
            subject='Hello',
            content='I wanna ask a question about your apache content',
            ip='127.0.0.1',
        )
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='Of course, what is the problem, how can I help you?',
            ip='127.0.0.1',
        )
        sender_message = Message.objects.create(
            sender=sender,
            user=user,
            subject='Re:Hello',
            content='Thank you for your answer bla.. bla..',
            ip='127.0.0.1',
        )
        sender_message.is_delete = True
        sender_message.save()
        Message.objects.create(
            sender=user,
            user=sender,
            subject='re:Hello',
            content='....sure...',
            ip='127.0.0.1',
        )
        messages = Message.objects.outbox(user=user).order_by('id')
        self.assertEqual(messages.count(), 2)
