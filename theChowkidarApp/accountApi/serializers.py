from rest_framework import serializers
from theChowkidarApp.models import User, AccountVerify
from theChowkidarApp.helper import send_otp_via_email
import random

class AccountVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountVerify
        fields = ['email']

    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        if send_otp_via_email(validated_data['email'], otp):
            obj = AccountVerify.objects.update_or_create(email=validated_data['email'], otp=otp)
            return obj

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']