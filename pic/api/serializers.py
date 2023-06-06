from rest_framework import serializers
from picfetcher.models import content
from django.contrib.auth.models import User
from accounts.models import userprofile
from accounts.models import notify

class contentSerializer(serializers.ModelSerializer):

    thumbnail = serializers.ImageField(use_url=True)
    processedimg = serializers.ImageField(use_url=True)


    class Meta:

        model = content
        fields ="__all__"

class notifyserializer(serializers.ModelSerializer):

    class Meta:
        model = notify
        fields = "__all__"