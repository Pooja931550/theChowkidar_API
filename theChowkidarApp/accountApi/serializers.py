from rest_framework import serializers
from theChowkidarApp.models import User

class SendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_no', 'profile_pic']

class RegisterVaiPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_no', 'password']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_pic']

class ForgetPasswordSerializer(serializers.Serializer):
   pass
