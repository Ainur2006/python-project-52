from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses')}")

    def test_list(self):
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, 'Новый')

    def test_create(self):
        response = self.client.post(reverse('status_create'), {'name': 'Готов'})
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='Готов').exists())

    def test_create_duplicate(self):
        response = self.client.post(reverse('status_create'), {'name': 'Новый'})
        self.assertContains(response, 'already exists')

    def test_update(self):
        url = reverse('status_update', args=[1])
        response = self.client.post(url, {'name': 'Начат'})
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Status.objects.get(pk=1).name, 'Начат')

    def test_delete(self):
        response = self.client.post(reverse('status_delete', args=[2]))
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(pk=2).exists())