from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.generic.base import View


class IndexView(View):

    def get(self, request):
        return HttpResponse('Hello!')


