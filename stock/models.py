from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, is_staff=False, is_admin=False, is_active=True, confirmedEmail=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a nickname")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.confirmedEmail = confirmedEmail
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            is_staff=True,
            is_admin=True,
            confirmedEmail=False,
        )
        return user

class User(AbstractUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    username = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    confirmedEmail = models.BooleanField(default=False)
    dateRegistered = models.DateTimeField(
        auto_now_add=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "<%d %s>" %(self.pk,self.email)
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active