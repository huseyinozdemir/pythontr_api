from unittest.mock import patch, Mock

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CONTACT_URL = reverse('contact:send')

VALID = {
    'name': 'Ayşe',
    'email': 'ayse@example.com',
    'subject': 'Pedal çalışmıyor',
    'message': 'Bluetooth pedal Mac üzerinde bağlanıyor ama tuş göndermiyor.',
    'app': 'Promptella',
    'app_version': '1.0.0',
}


@override_settings(CONTACT_EMAIL='destek@example.com',
                   DEFAULT_FROM_EMAIL='noreply@example.com')
class ContactApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def test_sends_mail_to_owner_with_reply_to(self):
        res = self.client.post(CONTACT_URL, VALID, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ['destek@example.com'])
        self.assertEqual(msg.from_email, 'noreply@example.com')
        self.assertEqual(msg.reply_to, ['ayse@example.com'])
        self.assertEqual(msg.subject, '[Promptella] Pedal çalışmıyor')
        self.assertIn('Bluetooth pedal', msg.body)

    def test_response_does_not_leak_owner_address(self):
        res = self.client.post(CONTACT_URL, VALID, format='json')
        self.assertNotIn('destek@example.com', res.content.decode())

    def test_invalid_email_rejected(self):
        res = self.client.post(
            CONTACT_URL, {**VALID, 'email': 'yanlis'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_short_message_rejected(self):
        res = self.client.post(
            CONTACT_URL, {**VALID, 'message': 'kısa'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_too_long_message_rejected(self):
        res = self.client.post(
            CONTACT_URL, {**VALID, 'message': 'a' * 5001}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_honeypot_returns_ok_but_sends_nothing(self):
        res = self.client.post(
            CONTACT_URL, {**VALID, 'website': 'http://spam'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_newlines_in_subject_cannot_inject_headers(self):
        res = self.client.post(
            CONTACT_URL,
            {**VALID, 'subject': 'a\r\nBcc: x@evil.com'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        msg = mail.outbox[0]
        self.assertNotIn('\n', msg.subject)
        self.assertEqual(msg.bcc, [])

    def test_mail_failure_returns_500(self):
        with patch('contact.views.EmailMessage.send',
                   side_effect=OSError('smtp down')):
            res = self.client.post(CONTACT_URL, VALID, format='json')
        self.assertEqual(res.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @override_settings(CONTACT_REQUIRE_CAPTCHA=True,
                       RECAPTCHA_URL='https://captcha.test/verify')
    def test_captcha_required_when_enabled(self):
        res = self.client.post(CONTACT_URL, VALID, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(CONTACT_REQUIRE_CAPTCHA=True,
                       RECAPTCHA_URL='https://captcha.test/verify')
    def test_captcha_failure_rejected_and_success_accepted(self):
        with patch('contact.serializers.requests.post') as post:
            post.return_value = Mock(json=lambda: {'success': False})
            res = self.client.post(
                CONTACT_URL, {**VALID, 'captcha': 'x'}, format='json')
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            post.return_value = Mock(json=lambda: {'success': True})
            res = self.client.post(
                CONTACT_URL, {**VALID, 'captcha': 'x'}, format='json')
            self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_throttle_limits_requests(self):
        from rest_framework.throttling import ScopedRateThrottle
        with patch.object(ScopedRateThrottle, 'THROTTLE_RATES',
                          {'contact': '2/hour'}):
            codes = [self.client.post(CONTACT_URL, VALID, format='json')
                     .status_code for _ in range(3)]
        self.assertEqual(codes[:2], [200, 200])
        self.assertEqual(codes[2], status.HTTP_429_TOO_MANY_REQUESTS)
