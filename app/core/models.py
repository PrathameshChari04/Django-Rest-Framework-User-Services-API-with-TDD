from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('User must have an email message')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    

class Tag(models.Model):
    """ Tag to be used in services """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,


    )

    def __str__(self):
        return self.name


class Components(models.Model):
    """  Components to be used in service """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,

    )

    def __str__(self):
        return self.name

class Services(models.Model):
    """ Services Object """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    components = models.ManyToManyField('Components')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
    



    

