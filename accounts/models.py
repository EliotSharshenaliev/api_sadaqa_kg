import stripe
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from djstripe.fields import StripeIdField
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, firstname, lastname, phone, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.lastname = lastname
        user.firstname = firstname
        user.phone = phone

        stripe_id = self._create_user_stripe(
            name=firstname+" "+lastname,
            email=email,
            phone=phone,
            username=username
        )

        if not stripe_id:
            raise TypeError('Something went wrong. Try register again')

        user.stripe_id = stripe_id
        user.save()
        return user

    def create_superuser(self, firstname, lastname, phone, username, email, password=None):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(firstname, lastname, phone, username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    @staticmethod
    def _create_user_stripe(name, email, phone, username):
        try:
            customer = stripe.Customer.create(
                description=username,
                name=name,
                email=email,
                phone=phone,
            )
            return customer.id
        except Exception as e:
            print(e)
        return False


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    stripe_id = StripeIdField(max_length=500, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username
