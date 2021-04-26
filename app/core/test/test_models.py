from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_successful(self):
        """Test creating a user with a successful email"""
        username = "ddd@gmail.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=username, password=password)
        self.assertEqual(user.email, username[0])
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """test to assert that an email is not normalized"""
        username = "DDD@gmail.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email="ddd@gmail.com", password=password)
        self.assertNotEqual(user.email, username) 

    def test_new_user_invalid_email(self):
        """Trying to create a user with an invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password="password")

    def test_new_user_invalid_password(self):
        """Trying to create a user with an invalid password"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="ddd@gmail.com",password=None)  

    def test_new_super_user(self):
        """Trying a test on creating the super user"""
        email = "ddd@gmail.com"
        password = "password"
        user = get_user_model().objects.create_superuser(email=email,password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        