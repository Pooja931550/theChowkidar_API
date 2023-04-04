from rest_framework.views import APIView
from rest_framework.response import Response
from theChowkidarApp.models import User
from . serializers import SendOTPSerializer, RegisterVaiPhoneSerializer, UpdateProfileSerializer, UserProfileSerializer
from theChowkidarApp.helper import send_otp_via_email
from django.contrib.auth import authenticate
import random
from rest_framework import routers
router = routers.DefaultRouter()

class SendOtpViaEmailAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            user_obj = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            user_obj = None
        
        if user_obj is not None:
            otp = random.randint(1000, 9999)
            success = send_otp_via_email(data.get('email'), otp)
            if success:
                obj = User.objects.filter(email=data.get('email'))
                obj.update(otp=otp)
                obj.update(otp_expire=False)
                return Response({
                    'status': 200,
                    'message': 'OTP has been successfully send. Please check your email for verify!!'
                })
            return Response({
                'status': 202,
                'message': 'Something went wrong!!'
            })
        serializer = SendOTPSerializer(data=data)
        if serializer.is_valid():
            otp = random.randint(1000, 9999)
            success = send_otp_via_email(data.get('email'), otp)
            if success:
                serializer.save()
                obj = User.objects.filter(email=data.get('email'))
                obj.update(otp=otp)
                return Response({
                    'status': 200,
                    'message': 'OTP has been successfully send. Please check your email for verify!!'
                })
            return Response({
                'status': 202,
                'message': 'Something went wrong!!'
            })
        return Response({
            'status': 202,
            'message': 'Something went wrong!!',
            'errors': serializer.errors
        })

class VerifyEmailAPIView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(email=data.get('email')).first() is None:
            return Response({
                'status':202,
                'message': 'Email ID is wrong!!'
            })
        if User.objects.filter(otp=data.get('otp')).first() is None:
            return Response({
                'status':203,
                'message': 'OTP is wrong!!'
            })
        obj = User.objects.filter(email=data.get('email'), otp=data.get('otp')).first()
        if obj.otp_expire:
            return Response({
                'status': 205,
                'message': 'Your otp has been expired!!'
            })
        verify = User.objects.filter(email=data.get('email'))
        verify.update(is_verified=True)
        verify.update(otp_expire=True)
        return Response({
            'status':200,
            'message': 'Your email has been successfully verified!!'
        })

class RegisterVaiEmailAPIView(APIView):
    def post(self, request):
        data = request.data
        user_obj = User.objects.filter(email=data.get('email')).first()
        if user_obj is not None:
            if user_obj.is_created:
                return Response({
                    'status':203,
                    'message': 'Your account has been already exist!!'
                })
            if user_obj.is_verified:
                user = User.objects.get(email=data.get('email'))
                user.set_password(data.get('password'))
                user.save()
                user_created = User.objects.filter(email=data.get('email'))
                user_created.update(is_created=True)
                return Response({
                    'status':200,
                    'message': 'Your account has been successfully created!!'
                })
            return Response({
                'status':200,
                'message': "Your email id isn't verified!!"
            })

class LoginViaEmailAPIView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(request, email=data.get('email'), password=data.get('password'))
        if user is not None:
            obj = User.objects.get(id=user.id)
            serializer = UserProfileSerializer(obj)
            return Response({
                'status': 200,
                'message': 'Your account has been successfully logged in!!',
                'payload': serializer.data
            })
        return Response({
            'status': 202,
            'message': 'Login details are wrong. Please try again!!'
        })

class RegisterVaiPhoneAPIView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(phone_no=data.get('phone_no')).first() is not None:
            return Response({
                'status': 203,
                'message': 'Your phone number already exist!!'
            })
        serializer = RegisterVaiPhoneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'Your account has been successfully created!!'
            })
        return Response({
            'status': 202,
            'message': 'Something went wrong!!',
            'errors': serializer.errors
        })

class LoginVaiPhoneAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(phone_no=data.get('phone_no'), password=data.get('password'))
        except User.DoesNotExist:
            user=None
        if user is not None:
            obj = User.objects.get(id=user.id)
            serializer = UserProfileSerializer(obj)
            return Response({
                'status': 200,
                'message': 'Your account has been successfully logged in!!',
                'payload': serializer.data
            })
        return Response({
            'status': 200,
            'message': 'Your login details are wrong!!'
        })

class UpdateProfileAPIView(APIView):
    def put(self, request, pk):
        try:
            user_obj = User.objects.get(id=pk)
        except User.DoesNotExist:
            user_obj = None
        
        if user_obj is not None:
            serializer = UpdateProfileSerializer(user_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Your profile has been successfully updated!!',
                    'payload': serializer.data
                })
            return Response({
                'status': 202,
                'message': 'Something went wrong!!',
                'errors': serializer.errors
            })

class ForgetPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(email=data.get('email')).first() is None:
            return Response({
                'status':202,
                'message': 'Email ID is wrong!!'
            })
        if User.objects.filter(otp=data.get('otp')).first() is None:
            return Response({
                'status':203,
                'message': 'OTP is wrong!!'
            })
        obj = User.objects.filter(email=data.get('email'), otp=data.get('otp')).first()
        if obj.otp_expire:
            return Response({
                'status': 205,
                'message': 'Your otp has been expired!!'
            })
        if obj.is_created:
            reset = User.objects.filter(email=data.get('email'))
            obj.set_password(data.get('password'))
            obj.save()
            reset.update(otp_expire=True)
            return Response({
                'status':200,
                'message': 'Your password successfully changed!!'
            })
        return Response({
            'status':200,
            'message': "Your account isn't available!!"
        })

        
            