from django.test import TestCase
from django.shortcuts import reverse


# Create your tests here.

class LandingPagTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('landing_Page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")
