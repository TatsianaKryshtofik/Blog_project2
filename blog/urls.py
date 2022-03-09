from django.urls import path

from .views import *


app_name = 'blog'

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/update/', UserUpdateAPIView.as_view()),
    path('userinfo/', AddUserInfoAPIView.as_view({'post': 'create', 'get': 'list'})),
    path('userinfo/<int:pk>/', AddUserInfoAPIView.as_view({'put': 'update', 'get': 'retrieve'})),
    path('post/', PostAPIView.as_view({'post': 'create', 'get': 'list'})),
    path('post/<int:pk>/', PostAPIView.as_view({'put': 'update', 'get': 'retrieve'})),
    path('tag/', TagListAPIView.as_view()),
    path('category/', CategoryListView.as_view()),
    path('subcategory/', SubcategoryListAPIView.as_view()),
]
