from django.core.mail import send_mail
from django.conf import settings

def send_otp_via_email(email, otp):
    subject = 'Your account verification email!!'
    message = f'Your OTP is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    return True