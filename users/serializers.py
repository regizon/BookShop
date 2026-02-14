from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.services import get_user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "native_name", "phone_number")

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "native_name", "phone_number")



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class EmailVerifySerializerTest(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    native_name = serializers.CharField(required=False)

    def validate(self, data):
        email = data.get('email')
        if email is not None:
            if get_user(email) is not None:
                pass
            else:
                #if data.get('phone_number') is None or data.get('native_name') is None:
                if data.get('native_name') is None:
                    raise serializers.ValidationError('Phone number and native_name are required')
        else:
            raise serializers.ValidationError('Email is required')

        return data