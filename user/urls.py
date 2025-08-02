from django.urls import path


from . import views
from .views import user_login_view, logout_view

urlpatterns = [
    path('register/', views.user_register_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otp_verify/<int:user_id>/', views.otp_verify_view, name='otp_verify'),
]