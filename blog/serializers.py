from django.contrib.auth import authenticate

from .models import User, Post, UserInfo, Comment, Image, PostRating
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, email=email,
                            password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username
        }


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=50,
        min_length=6,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'subcategory', 'description', 'user']


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ['country', 'city', 'user']


class CommentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Comment
        fields = ['user', 'post', 'description']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image url', 'created_at']


class PostRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostRating
        fields = ['user', 'post', 'value']
