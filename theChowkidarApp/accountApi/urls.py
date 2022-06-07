from django.urls import path, include
from . import views

urlpatterns = [
    path('', include(views.router.urls)),
    path('send-otp/', views.SendOtpViaEmailAPIView.as_view()),
]

