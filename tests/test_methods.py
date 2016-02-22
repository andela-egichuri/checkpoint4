from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from faker import Factory
from app.models import Picture, Effect, EffectType

fake = Factory.create()


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = fake.email()
        self.username = fake.user_name()
        self.password = fake.password()
        self.initial_user = User.objects.create(
            username=fake.user_name(), password=fake.password(),
            email=fake.email()
        )

    def tearDown(self):
        del self.initial_user

    def test_index_view(self):
        """ Test the homepage view."""
        url = reverse('index')
        before_login = self.client.get(url)
        self.client.force_login(self.initial_user)
        after_login = self.client.get(url)
        self.assertEqual(before_login.status_code, 200)
        self.assertTemplateUsed(before_login, 'index.html')
        self.assertContains(before_login, 'Login to get started')
        self.assertEqual(after_login.status_code, 302)
        self.assertEqual(before_login.request['PATH_INFO'], '/')