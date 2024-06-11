from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    full_name = serializers.CharField()
    birth_date = serializers.DateField()

    def save(self, request):
        user = super().save(request)
        user.full_name = self.validated_data.get("full_name")
        user.birth_date = self.validated_data.get("birth_date")
        user.save()

        return user
