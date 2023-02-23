from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, reverse
import shutil
import os
import sys
import time

import undetected_chromedriver
from selenium.webdriver.common.by import By
import zipfile
import pandas as pd

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def all_hw2_view(request):
    pages = {
        'ДЗ пагинация': reverse('pagi'),
        'ДЗ рецепты': reverse('calculator'),
    }

    context = {
        'pages': pages
    }
    return render(request, 'all_hw2.html', context)


def all_recept_view(request):
    pages = {
        'Рецепт Омлета': reverse('omlet_view'),
        'Рецепт Пасты': reverse('pasta_view'),
        'Рецепт бутерброда': reverse('buter_view'),
        # 'Главная страница': reverse('home_hw2'),
    }

    context = {
        'pages': pages
    }
    return render(request, 'all_recept_view.html', context)


def omlet_view(request):
    servings = int(request.GET.get('servings', 1))
    omlet_recept = {name: servings * count for name, count in DATA['omlet'].items()}
    context = {
        'omlet_rec': omlet_recept,
        'home_hw2': reverse('home_hw2'),
        'all_rec': reverse('all_rec'),
    }
    return render(request, 'omlet_view.html', context)


def pasta_view(request):
    servings = int(request.GET.get('servings', 1))
    omlet_recept = {name: servings * count for name, count in DATA['pasta'].items()}
    context = {
        'pasta_rec': omlet_recept,
        'home_hw2': reverse('home_hw2'),
        'all_rec': reverse('all_rec'),
    }
    return render(request, 'pasta_view.html', context)


def buter_view(request):
    servings = int(request.GET.get('servings', 1))
    omlet_recept = {name: servings * count for name, count in DATA['buter'].items()}
    context = {
        'buter_rec': omlet_recept,
        'home_hw2': reverse('home_hw2'),
        'all_rec': reverse('all_rec'),
    }
    return render(request, 'buter_view.html', context)


########################## Это файл для домашки в Нетологии по Джанго ######################
def get_selenium_open_data_moscow_stops():
    """
    Selenium заходит на урл с остановками (константа) и скачивает файл(зип архив) с расположением остановок в МСК.
    Поиск элементов по XPATH (Установлен невидимый режим)
    :return: Ничего не возвращает, просто скачивает файл
    """
    url = 'https://data.mos.ru/opendata/752?pageNumber=2&versionNumber=8&releaseNumber=8'
    options = undetected_chromedriver.options.ChromeOptions()
    options.add_argument("--headless=new")
    browser = undetected_chromedriver.Chrome(options=options)
    browser.get(url)
    browser.set_window_size(1920, 1080)
    browser.implicitly_wait(30)
    browser.find_element(By.XPATH, '//*[@id="dropDepartmentsLink"]').click()
    time.sleep(2)
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/li[2]/div/a').click()
    time.sleep(5)
    return HttpResponse


def get_file_open_data_in_downloads(request):
    """
    Получает список файлов в папке "Загрузки", далее выбирает самый последний файл по времени создания (там должен
    находится наш зип архив с сайта с остановками), далее идет проверка на существование папки, куда будет распаковываться
    зип архив, если ее нет, то создает, если она есть , то сначала перемещает архив туда, потом распаковывает архив (
    там находится файл в формате xlsx), далее оставляет только xlsx и удаляет зип.
    :return:
    """
    new_folder = 'selenium_downloads'
    file_destination = os.getcwd() + rf'\{new_folder}'
    path_with_xlsx = file_destination + fr'\{os.listdir(file_destination)[0]}'
    if not os.path.exists(path_with_xlsx):

        get_selenium_open_data_moscow_stops()
        file_source = r'C:\Users\Владелец\Downloads'
        file_list = os.listdir(file_source)
        files = [os.path.join(file_source, file) for file in file_list]
        zip_file_selenium = max(files, key=os.path.getctime)

        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        zip_file_path = shutil.move(str(zip_file_selenium), str(file_destination))

        fantasy_zip = zipfile.ZipFile(zip_file_path)
        fantasy_zip.extractall(file_destination)
        fantasy_zip.close()

        os.remove(zip_file_path)

    df = pd.DataFrame(pd.read_excel(path_with_xlsx))
    list_with_name_in_pd = ["Name",'Longitude_WGS84', 'Latitude_WGS84', 'AdmArea', 'District',
                            'RouteNumbers', 'StationName', 'Direction', 'Pavilion', 'OperatingOrgName',
                            'EntryState', 'global_id', 'PlaceDescription']
    clear_df = pd.DataFrame()
    for el in list_with_name_in_pd:
        clear_df[el] = df[el]
    # pandas_list = [df[name].tolist() for name in list_with_name_in_pd]

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(clear_df, 100)
    page = paginator.get_page(page_number)
    context = {
        'clear_df': clear_df,
        'list_with_name_in_pd': list_with_name_in_pd,
        'home_hw2': reverse('home_hw2'),
        'page': page
    }
    return render(request, 'stops_view.html', context)



# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
# Create your views here.
