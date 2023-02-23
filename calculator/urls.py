
from django.urls import path
from calculator.views import all_hw2_view, omlet_view, buter_view, pasta_view, all_recept_view, \
    get_file_open_data_in_downloads

urlpatterns = [
    path('', all_hw2_view, name='home_hw2'),
    path('omlet/', omlet_view, name='omlet_view'),
    path('pasta/', pasta_view, name='pasta_view'),
    path('buter/', buter_view, name='buter_view'),
    path('all_rec/', all_recept_view, name='all_rec'),
    path('pagi/', get_file_open_data_in_downloads, name='pagi'),
    # path('calculator/', workdir_view, name='calculator'),
    # path('workdir_pagination/', pagination_workdir_view, name='pagi_work'),
]