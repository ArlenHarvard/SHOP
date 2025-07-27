from django.urls import path
from .views import detail_view, index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('detail/', detail_view, name='detail'),
]
