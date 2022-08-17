from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pyshorteners.exceptions import BadURLException
from django.db.models import Count
from .forms import *
import pyshorteners
from django.views.generic import CreateView, ListView
from .models import *
from django.contrib.auth.models import User
from hashids import Hashids


def convert_url(request):
    context = {}
    if request.method == 'POST':
        form = ConvertForm(request.POST)
        if form.is_valid():
            try:
                url_obj = URL.objects.get(long_url=form.cleaned_data['long_url'])
            except :
                url_obj = None
            if not url_obj:
                hashid = Hashids(salt=form.cleaned_data['long_url'])
                short_url = hashid.encode(1, 2, 3)
                form.cleaned_data['short_url'] = short_url
                context['short_link'] = short_url
                if request.user.is_authenticated:
                    user = User.objects.get(username=request.user.username)
                    form.cleaned_data['user'] = user
                link_obj = URL.objects.create(**form.cleaned_data)
                context['link_obj'] = link_obj
            if url_obj:
                user = request.user
                form.cleaned_data['user'] = user
                if not url_obj.user:
                    if url_obj.user != user:
                        print(url_obj.user, url_obj.user.username, user)
                        URL.objects.create(**form.cleaned_data)
                context['link_obj'] = url_obj
                context['short_link'] = url_obj.short_url
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
    model = URL
    context_object_name = 'urls'
    login_url = 'login'
    template_name = 'main/history.html'
    allow_empty = True

    def get_queryset(self):
        return URL.objects.filter(user=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История'
        return context


def get_redirect(request, url_pk):
    url_obj = URL.objects.get(pk=url_pk)
    return redirect(url_obj.long_url)
