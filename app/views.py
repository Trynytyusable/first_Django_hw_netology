import datetime
import os
import platform

from django.core.paginator import Paginator
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
        'Показать содержимое рабочей директории постранично': reverse('pagi_work'),
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
        'os_user': osp,
        'home_page': reverse('home'),
    }
    return render(request, template_name, context)


list_of_dir = os.listdir(".")


def workdir_view(request):
    workdir_template = 'app/workdir_template.html'
    context = {
        'list_dir': list_of_dir,
        'home_page': reverse('home'),
    }

    return render(request, workdir_template, context)


def pagination_workdir_view(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(list_of_dir, 2)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'page_number': page_number,
        'previous_page': page_number - 1,
        'next_page': page_number + 1,
        'home_page': reverse('home'),
    }
    return render(request, 'app/workdir_pagination.html', context)