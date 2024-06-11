from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
