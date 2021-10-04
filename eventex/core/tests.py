from django.test import TestCase

# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def text_subscription_link(self):
        self.assertContains(self.response,'href="/inscricao/"')
