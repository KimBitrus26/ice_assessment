import email
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from accounts.serializers import CustomUserDetailsSerializer

CREATE_USER_URL = "/api/v1/auth/registration/"
LOGIN_URL = "/api/v1/auth/login/"


def create_user(**params):
    return User.objects.create_user(**params)


class AUTHRegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test create user is successfull"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john",
            "password": "johnpassword123"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertIn("access_token", res.data)
        self.assertEqual(res.data['user']['full_name'], payload['full_name'])
        self.assertEqual(res.data['user']['email'], payload['email'])

    def test_create_user_already_exist(self):
        """Test emali already exists"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "johnpassword123"
        }
        payload1 = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "johnpassword123"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short(self):
        """Test password too short"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "jd1"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_user_loggedin(self):
        """Test user loggedin is successfull"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "password@1234"
        }
        self.client.post(CREATE_USER_URL, payload)
        payload1 = {
            "email": payload["email"],
            "password": payload["password"]
        }
        res = self.client.post(LOGIN_URL, payload1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", res.data)
        self.assertEqual(res.data['user']['email'], payload['email'])

    def test_user_logged_in_wrong_password(self):
        """Test user login with wrong password"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "password@1234"
        }
        self.client.post(CREATE_USER_URL, payload)
        payload = {
            "email": payload["email"],
            "password": "wrongpassword231"
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", res.data)

    def test_user_log_in_wrong_email(self):
        """Test user login with wrong email"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john",
            "password": "password@1234"
        }
        self.client.post(CREATE_USER_URL, payload)
        payload = {
            "email": "wrong@gmail.com",
            "password": payload["password"],
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", res.data)

    def test_user_log_in_blank_email(self):
        """Test user login with blank email"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "password@1234",
        }
        self.client.post(CREATE_USER_URL, payload)
        payload = {
            "email": "",
            "password": payload["password"],
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", res.data)

    def test_user_log_in_blank_password(self):
        """Test user login with blank password"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "password@1234"
        }
        self.client.post(CREATE_USER_URL, payload)
        payload = {
            "email": payload["email"],
            "password": ""
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", res.data)

    def test_user_log_in_invalid_email(self):
        """Test user login with invalid email"""

        payload = {
            "email": "john@gmail.com",
            "full_name": "john doe",
            "password": "password@1234"
        }
        self.client.post(CREATE_USER_URL, payload)
        payload = {
            "email": "johngmail.com",
            "password": payload["password"],
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access_token", res.data)

    def test_create_user_with_no_data(self):
        """test to create a new user without sending data"""

        res = self.client.post(CREATE_USER_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
