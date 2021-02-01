from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTestCase(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user_obj = User.objects.create_user(email='user@email.com', password='foo')

        self.assertEqual(user_obj.email, 'user@email.com')
        self.assertTrue(user_obj.is_active)
        self.assertFalse(user_obj.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        user_obj = User.objects.create_superuser(email='superuser@email.com', password='bar')

        self.assertEqual(user_obj.email, 'user@email.com')
        self.assertTrue(user_obj.is_active)
        self.assertTrue(user_obj.is_staff)
