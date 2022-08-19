from django.test import TestCase
from .models import Act

class ActTestCase(TestCase):
    def setUp(self):
        Act.objects.create(name="lion", sound="roar")
        Act.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Act.objects.get(name="lion")
        cat = Act.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')