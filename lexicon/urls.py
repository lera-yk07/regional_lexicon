from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('compare/', views.compare_cities, name='compare'),
    path('statistics/', views.statistics, name='statistics'),
    path('register/', views.register, name='register'),
    path('add-word/', views.add_word, name='add_word'),
    path('word/<int:pk>/', views.word_detail, name='word_detail'),
    path('region/<int:pk>/', views.region_detail, name='region_detail'),
    path('city/<int:pk>/', views.city_detail, name='city_detail'),
]