import datetime
import os
import platform

from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    template_name = 'app/times.html'
    current_time = datetime.datetime.now().time()
    osp = platform.platform()
    context = {
        'times': current_time,
        'os_user': osp
    }
    return render(request, template_name, context)


def workdir_view(request):
    workdir_template = 'app/workdir_template.html'
    list_of_dir = os.listdir(".")
    context = {
        'list_dir': list_of_dir
    }

    return render(request, workdir_template, context)
