import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label='Статус',
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label='Исполнитель',
    )
    label = django_filters.ModelChoiceFilter(
        field_name='labels', queryset=Label.objects.all(), label='Метка',
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['executor'].label_from_instance = (
            lambda user: user.get_full_name() or user.username
        )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset