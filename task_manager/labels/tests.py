from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Label


class LabelCRUDTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('labels'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels')}")

    def test_list(self):
        self.assertContains(self.client.get(reverse('labels')), 'Баг')

    def test_create(self):
        response = self.client.post(reverse('label_create'), {'name': 'Срочно'})
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='Срочно').exists())

    def test_create_duplicate(self):
        response = self.client.post(reverse('label_create'), {'name': 'Баг'})
        self.assertContains(response, 'already exists')

    def test_update(self):
        response = self.client.post(reverse('label_update', args=[2]), {'name': 'Улучшение'})
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(Label.objects.get(pk=2).name, 'Улучшение')

    def test_delete_unused(self):
        response = self.client.post(reverse('label_delete', args=[3]))
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(pk=3).exists())

    def test_delete_used_denied(self):
        response = self.client.post(reverse('label_delete', args=[1]), follow=True)
        self.assertContains(response, 'Невозможно удалить метку')
        self.assertTrue(Label.objects.filter(pk=1).exists())