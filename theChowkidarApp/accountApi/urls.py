from django.urls import path, include
from . import views

urlpatterns = [
    path('', include(views.router.urls)),
    path('send-otp-via-email/', views.SendOtpViaEmailAPIView.as_view()),
    path('verify-email/', views.VerifyEmailAPIView.as_view()),
    path('register-via-email/', views.RegisterVaiEmailAPIView.as_view()),
    path('login-via-email/', views.LoginViaEmailAPIView.as_view()),
    path('register-via-phone/', views.RegisterVaiPhoneAPIView.as_view()),
    path('login-via-phone/', views.LoginVaiPhoneAPIView.as_view()),
    path('update-profile/<int:pk>/', views.UpdateProfileAPIView.as_view()),
    path('forget-password/', views.ForgetPasswordAPIView.as_view()),
]

