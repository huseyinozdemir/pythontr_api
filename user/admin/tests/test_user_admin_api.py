from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class UserAdminAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.admin_user)

        self.regular_user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
            is_staff=False,
            is_superuser=False
        )

    def test_list_users(self):
        """Test retrieving a list of users"""
        url = reverse('user:admin:users-list')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 2)

    def test_user_detail(self):
        """Test retrieving user details"""
        url = reverse('user:admin:users-detail', args=[self.regular_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.regular_user.email)
        self.assertEqual(res.data['name'], self.regular_user.name)

    def test_create_user(self):
        """Test creating a new user through admin API"""
        url = reverse('user:admin:users-list')
        payload = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'name': 'New User'
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_update_user(self):
        """Test updating user through admin API"""
        url = reverse('user:admin:users-detail', args=[self.regular_user.id])
        payload = {
            'name': 'Updated Name'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.name, payload['name'])

    def test_delete_user(self):
        """Test deleting user through admin API"""
        url = reverse('user:admin:users-detail', args=[self.regular_user.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            get_user_model().objects.filter(id=self.regular_user.id).exists()
        )
