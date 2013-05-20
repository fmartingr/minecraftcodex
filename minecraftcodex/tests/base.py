from django.test import TestCase
from django.conf import settings


class SettingsTest(TestCase):
    def test_local_settings(self):
        self.assertTrue(settings.LOCAL_SETTINGS)
