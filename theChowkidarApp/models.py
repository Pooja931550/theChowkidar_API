from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

#================= Model for user account ====================#
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    phone_no = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/user/profile/%Y/%m/%d/', null=True, blank=True)
    otp = models.IntegerField(default=0)
    otp_expire = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_created = models.BooleanField(default=False)
    role = models.CharField(max_length=150, default='subscriber')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)


