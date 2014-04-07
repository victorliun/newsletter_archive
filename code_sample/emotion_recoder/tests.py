"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import Emotions


class SimpleTest(TestCase):
    """ Test Model Emotions."""
    def setUp(self):
        Emotions.objects.create(description="What a nice day", author=test_author)
        Emotions.objects.create(description="I don't like rain", author=test_author)

    def test_model_save_func(self):
        """
        Save function should be able to set previous recorder to less latest
        """

        em1 = Emotions.objects.get(description="What a nice day")
        em2 = Emotions.objects.get(description="I don't like rain")
        self.assertEqual(em1.latest, False)
        self.assertEqual(em2.latest, True)

    
