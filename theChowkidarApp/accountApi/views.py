from rest_framework.views import APIView
from rest_framework.response import Response
from theChowkidarApp.models import AccountVerify
from . serializers import AccountVerifySerializer
from rest_framework import routers
router = routers.DefaultRouter()

class SendOtpViaEmailAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            user_obj = AccountVerify.objects.get(email=data.get('email'))
        except AccountVerify.DoesNotExist:
            user_obj = None
        
        if user_obj is None:
            serializer = AccountVerifySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'OTP has been successfully send. Please check your email for verify!!'
                })
            return Response({
                'status': 202,
                'message': 'Something went wrong!!',
                'errors': serializer.errors
            })
        return Response({
            'status': 203,
            'message': 'Your email ID already exist!!'
        })
            