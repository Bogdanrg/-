from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
import pyshorteners
from django.views.generic import CreateView, ListView
from .models import *
from django.contrib.auth.models import User


def convert_url(request):
    context = {}
    if request.method == 'POST':
        form = ConvertForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['url']
            s = pyshorteners.Shortener()
            context['short_link'] = s.tinyurl.short(link)
            form.cleaned_data['url'] = s.tinyurl.short(link)
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user.username)
                form.cleaned_data['user'] = user
                HistoryURLs.objects.create(**form.cleaned_data)
    else:
        form = ConvertForm()
    c_def = {'form': form, 'title': 'Главная страница'}

    return render(request, template_name='main/converter.html', context={**c_def, **context})


class RegistrationUserView(CreateView):
    form_class = RegistrationUserForm
    success_url = reverse_lazy('login')
    template_name = 'main/registration.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вxод'
        return context


def logout_user(request):
    logout(request)
    return redirect('home')


class HistoryView(LoginRequiredMixin, ListView):
    model = HistoryURLs
    context_object_name = 'urls'
    login_url = 'login'
    template_name = 'main/history.html'
    allow_empty = True

    def get_queryset(self):
        return HistoryURLs.objects.filter(user=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История'
        return context
