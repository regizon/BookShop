from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "native_name", "phone_number")

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "native_name", "phone_number")

    def create(self, validated_data):
        email = validated_data.get("email")
        native_name = validated_data.get("native_name")
        phone_number = validated_data.get("phone_number")

        user = get_user_model()
        new_user = user.objects.create_user(email=email, native_name=native_name, phone_number=phone_number)
        new_user.set_unusable_password()
        new_user.save()
        return new_user

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()