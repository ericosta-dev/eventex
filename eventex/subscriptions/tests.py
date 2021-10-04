from django.http import response
from django.test import TestCase
from django.core import mail

from eventex.subscriptions.forms import SubscriptionForm

# Create your tests here.
class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Eric Costa',cpf='12345678901',email='ericosta.dev@gmail.com'
        , phone='84-99676-5969')
        self.resp = self.client.post('/inscricao/',data)

    def test_post(self):
        self.assertEqual(302,self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1,len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect,email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'ericosta.dev@gmail.com'

        self.assertEqual(expect,email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br','ericosta.dev@gmail.com']

        self.assertEqual(expect,email.to)
    
    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Eric Costa',email.body)
        self.assertIn('12345678901',email.body)
        self.assertIn('ericosta.dev@gmail.com',email.body)
        self.assertIn('84-99676-5969',email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/',{})

    def test_post(self):
        self.assertEqual(200,self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form,SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name='Eric Costa',cpf='12345678901',
        email = 'ericosta.dev@gmail.com',phone='84-996765969')
        response = self.client.post('/inscricao/',data,follow=True)
        self.assertContains(response,'Inscrição Realizada com Sucesso!')
 