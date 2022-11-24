from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelUserTests(TestCase):
    def setUp(self):
        self.email = "test@gmail.com"
        self.full_name = "John Doe"
        self.password = "test@b1234"
        self.user = User.objects.create_user(
            email=self.email,
            full_name=self.full_name,
            password=self.password
        )

    def test_user_model(self):
        """Test user instance is an object User"""

        user = self.user
        self.assertTrue(isinstance(user, User))

    def test_create_user_with_email(self):
        """Test creating new user with email not username"""

        self.assertEqual(self.user.email, self.email)

    def test_create_user_data_attributes(self):
        """Test creating new user is successfull"""

        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.full_name, self.full_name)
        self.assertTrue(self.user.check_password(self.password))


    def test_new_user_email_is_none(self):
        """Test create new user with no email raises error"""

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None, password="pass123", full_name="John Doe"
            )

    def test_create_new_supersuer(self):
        """Test creating new superuser"""

        super_user = User.objects.create_superuser(
            email="super@email.com", password="admn123"
        )
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
