from django.urls import path
from . import views  # импортируем весь модуль views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('detail/<int:estate_pk>/', views.detail_view, name='detail'),

    #Likes
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('favorite_list/', views.favorite_list_view, name='favorite_list' ),
    path('feedback/<int:estate_id>/create/', views.user_estate_feedback, name='feedback' ),
    path("estates/", views.estate_list_view, name="estate_list"),

]
