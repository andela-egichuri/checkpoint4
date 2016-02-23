import shutil
import tempfile
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings
from faker import Factory
from app.models import Picture, Effect, EffectType
from app.forms import ImageUploadForm

fake = Factory.create()


class BaseTestCase(TestCase):

    def setUp(self):
        """ Initialize test resources."""
        settings._original_media_root = settings.MEDIA_ROOT
        settings._original_file_storage = settings.DEFAULT_FILE_STORAGE
        self._temp_media = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self._temp_media
        settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

        self.email = fake.email()
        self.username = fake.user_name()
        self.password = fake.password()
        self.initial_user = User.objects.create(
            username=fake.user_name(), password=fake.password(),
            email=fake.email()
        )
        self.dash_url = reverse('dashboard')
        self.effect_types = {
            'image': ['rotate'],
            'imageenhance': ['enhance'],
            'imagefilter': ['smooth', 'emboss', 'contour', 'sharpen',
                            'findedges', 'blur', ],
            'imageops': ['flip', 'mirror', 'grayscale']
        }
        self.effects = []
        for item, value in self.effect_types.items():
            eff = EffectType.objects.create(name=item)
            for effect in value:
                self.effects.append(effect)
                Effect.objects.create(name=effect, effect_type=eff, status=1)

    def tearDown(self):
        """ Free resources and do some housekeeping after tests are run."""
        del self.initial_user
        shutil.rmtree(self._temp_media, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root
        settings.DEFAULT_FILE_STORAGE = settings._original_file_storage
        del settings._original_file_storage

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

    def test_dashboard_view(self):
        """ Test the dashboard view (Restricted)"""
        before_login = self.client.get(reverse('dashboard'))
        self.client.force_login(self.initial_user)
        after_login = self.client.get(reverse('dashboard'))
        self.assertEqual(before_login.status_code, 302)
        self.assertEqual(after_login.status_code, 200)

    def test_file_upload(self):
        """ Test the file upload functionality. """
        with open('tests/f.jpeg', 'rb') as fobj:
            data = {
                'image': fobj
            }
            up_test_no_auth = self.client.post(self.dash_url, data)
            self.assertEqual(up_test_no_auth.status_code, 302)

        self.client.force_login(self.initial_user)
        with open('tests/f.jpeg', 'rb') as fobj:
            data = {
                'image': fobj
            }
            up_test_after_auth = self.client.post(self.dash_url, data)
            self.assertEqual(up_test_after_auth.status_code, 200)

    def test_image_edit(self):
        self.client.force_login(self.initial_user)
        with open('tests/f.jpeg', 'rb') as fobj:
            data = {
                'image': fobj
            }
            uploaded_file = self.client.post(self.dash_url, data)
            file_id = uploaded_file.context['new_files'][0]

        self.edit_url = reverse('edit')

        for effect in self.effects:
            pic_data = {
                'id': file_id,
                'effect': effect
            }
            if effect == 'enhance':
                pic_data['color'] = 0.5
                pic_data['contrast'] = 0.5
                pic_data['sharpness'] = 0.5
                pic_data['brightness'] = 0.5
            apply_effect = self.client.post(self.edit_url, pic_data)
            self.assertEqual(apply_effect.status_code, 200)
            self.assertIsInstance(apply_effect.json(), dict)
            self.assertContains(apply_effect, effect)

    def test_get_image(self):
        self.client.force_login(self.initial_user)
        with open('tests/f.jpeg', 'rb') as fobj:
            data = {
                'image': fobj
            }
            uploaded_file = self.client.post(self.dash_url, data)
            file_id = uploaded_file.context['new_files'][0]
        image_data = {
            'id': file_id
        }

        get_image = self.client.post(reverse('image'), image_data)
        self.assertIsInstance(get_image.json(), dict)
        self.assertEqual(get_image.status_code, 200)
        self.assertContains(get_image, 'thumbnail')


