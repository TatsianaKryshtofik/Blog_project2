import jwt

from django.contrib.auth import user_logged_in
from rest_framework import status, generics

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler

from .classes import MixedSerializer, MixedPermission
from .serializers import *

from django.contrib.auth import authenticate


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        user = serializer.is_valid(raise_exception=True)

        try:
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            user = authenticate(email=email, username=username, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['username'] = user.username
                    user_details['email'] = user.email
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given '
                             'credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)


class UserUpdateAPIView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddUserInfoAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostAPIView(MixedSerializer, MixedPermission, ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PostListSerializer
    serializer_classes_by_action = {
        "create": PostSerializer,
        "update": PostSerializer,
        "retrieve": PostDetailSerializer
    }

    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "update": (IsAuthenticated,),
    }

    def get_queryset(self):
        if self.action == 'update':
            return Post.objects.filter(user=self.request.user)
        else:
            return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_middle_value(self):
        return Post.objects.all().annotate(
            middle_value=models.Sum(models.F('value')) / models.Count(models.F('value'))
        )


class RatingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatePostRatingSerializer


    def post(self, request):
        if not MyRating.objects.filter(user=request.user, post=request.data["post"]).exists():
            serializer = CreatePostRatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(status=201)
            else:
                return Response(status=400)
        else:
            return Response(status=400)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class SubcategoryListAPIView(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer
