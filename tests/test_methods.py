from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from app.models import Picture, Effect, EffectType


class BaseTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


