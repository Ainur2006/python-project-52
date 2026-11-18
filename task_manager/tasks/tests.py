from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskCRUDTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other = User.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks')}")

    def test_list_and_detail(self):
        self.assertContains(self.client.get(reverse('tasks')), 'Задача 1')
        self.assertContains(self.client.get(reverse('task_detail', args=[1])), 'Описание')

    def test_create_sets_author(self):
        data = {'name': 'Новая', 'description': '', 'status': 1, 'executor': ''}
        response = self.client.post(reverse('task_create'), data)
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(Task.objects.get(name='Новая').author, self.user)

    def test_create_duplicate(self):
        data = {'name': 'Задача 1', 'description': '', 'status': 1}
        response = self.client.post(reverse('task_create'), data)
        self.assertContains(response, 'already exists')

    def test_update(self):
        data = {'name': 'Изменена', 'description': '', 'status': 2, 'executor': ''}
        response = self.client.post(reverse('task_update', args=[1]), data)
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(Task.objects.get(pk=1).name, 'Изменена')

    def test_delete_by_author(self):
        response = self.client.post(reverse('task_delete', args=[1]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=1).exists())

    def test_delete_by_other_user_denied(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('task_delete', args=[1]), follow=True)
        self.assertContains(response, 'Задачу может удалить только ее автор')
        self.assertTrue(Task.objects.filter(pk=1).exists())


class TaskFilterTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))
        self.url = reverse('tasks')

    def test_no_filters(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 2')

    def test_filter_by_status(self):
        response = self.client.get(self.url, {'status': 1})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_by_executor(self):
        response = self.client.get(self.url, {'executor': 2})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_by_label(self):
        response = self.client.get(self.url, {'label': 2})
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Задача 1')

    def test_only_own_tasks(self):
        response = self.client.get(self.url, {'self_tasks': 'on'})
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')