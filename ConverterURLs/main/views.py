from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
import pyshorteners
from django.views.generic import ListView, DetailView, CreateView, FormView


def convert_url(request):
    context = {}
    if request.method == 'POST':
        form = ConvertForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['long_url']
            s = pyshorteners.Shortener()
            context['short_link'] = s.tinyurl.short(link)
    else:
        form = ConvertForm()
    c_def = {'form': form, 'title': 'Главная страница'}

    return render(request, template_name='main/converter.html', context={**c_def, **context})


# class ConvertURL(FormView):
# form_class = ConvertForm
# template_name = 'main/converter.html'
# success_url = reverse_lazy('home')

# def get_context_data(self, *, object_list=None, **kwargs):
# context = super().get_context_data(**kwargs)
# return context

class RegistrationUserView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')




def history(request):
    pass
