from .models import *
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone_number',
                  'password', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        user = User(email=self.validated_data['email'], username=self.validated_data['username'],
                    first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                    phone_number=self.validated_data['phone_number'])
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
        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return data


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



