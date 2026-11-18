from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    queryset = Task.objects.select_related('status', 'author', 'executor')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'
    extra_context = {'title': 'Создать задачу', 'button': 'Создать'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно изменена'
    extra_context = {'title': 'Изменение задачи', 'button': 'Изменить'}


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, 'Задачу может удалить только ее автор')
        return redirect('tasks')