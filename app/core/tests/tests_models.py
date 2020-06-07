from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from core.models import Tag, Components, Services

def sample_user(email='test@test.com', password='testpassword'):
    """ Create Sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = "test@gmail.com"
        password = "Test12345"
        user = get_user_model().objects.create_user(

            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email,'Test12345')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Test12345')

    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(

            'test@gmail.com',
            'test12345'


        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test the tag String representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Electrical'
        )

        self.assertEqual(str(tag), tag.name)

    def test_components_str(self):
        """ test the components String representation """
        components = models.Components.objects.create(
            user=sample_user(),
            name='H/w distribution'
        )

        self.assertEqual(str(components), components.name)


    def test_services_str(self):
        """ Test the job string representation """

        services = models.Services.objects.create(
            user=sample_user(),
            title='Title of the se',
            price=5.00
        )
        self.assertEqual(str(services), services.title)