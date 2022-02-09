from django.urls import path

from .views import *


app_name = 'blog'

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/update/', UserUpdateAPIView.as_view()),

]
