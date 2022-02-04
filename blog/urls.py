from django.urls import path

from .views import *
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

app_name = 'blog'

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view()),
    path('users/all/', UserListAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/update/', UserRetrieveUpdateAPIView.as_view()),
    path('posts/', PostAPIView.as_view()),
    path('userinfo/', UserInfoAPIView.as_view()),
    path('post/comment/', CommentAPIView.as_view()),
    path('image/', ImageAPIView.as_view()),
    path('post/rating/', PostRatingAPIView.as_view()),


]
