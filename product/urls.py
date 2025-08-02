from django.urls import path
from . import views  # импортируем весь модуль views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('detail/<int:estate_pk>/', views.detail_view, name='detail'),

    #Likes
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('favorite_list/', views.favorite_list_view, name='favorite_list' ),
]
