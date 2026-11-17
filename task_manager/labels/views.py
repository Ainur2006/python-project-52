from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'
    extra_context = {'title': 'Создать метку', 'button': 'Создать'}


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно изменена'
    extra_context = {'title': 'Изменение метки', 'button': 'Изменить'}


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно удалена'

    def form_valid(self, form):
        if self.object.tasks.exists():
            messages.error(self.request, 'Невозможно удалить метку')
            return redirect('labels')
        return super().form_valid(form)