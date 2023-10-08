import logging
import stripe
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from djstripe.fields import StripeIdField
from djstripe.models import Customer
logger = logging.getLogger(__name__)
from django.conf import settings

class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(
            self,
            username,
            email,
            lastname: str = "",
            firstname: str = "",
            phone: str = "",
            password=None,
            **extra_fields
    ):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.lastname = lastname
        user.firstname = firstname
        user.phone = phone
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    stripe_id = StripeIdField(max_length=500, null=True)
    stripe_user = models.BooleanField(
        verbose_name="This field need inform that user has created in stripe service",
        default=False,
        editable=False,
    )

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
        return "%s %s" % (self.firstname, self.lastname)

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def save(self, *args, **kwargs):

        if not self.stripe_user:
            self.__create_user_stripe()
        elif self.stripe_user:
            self.__update_stripe_customer()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.__delete_stripe_customer():
            super().delete(*args, **kwargs)

    def __create_user_stripe(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            description = self.get_full_name()
            customer = stripe.Customer.create(
                description=description,
                name=self.firstname,
                email=self.email,
                phone=self.phone,
            )
            self.stripe_id = customer.id
            self.stripe_user = True
            Customer.sync_from_stripe_data(customer)
            return customer.id
        except Exception as e:
            logger.error("Error: %s " % e.args)
            self.stripe_user =  False
            return False

    def __delete_stripe_customer(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.delete(self.stripe_id)
        except Exception as e:
            logger.info(e)

        return True

    def __update_stripe_customer(self) -> bool:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            description = self.get_full_name()
            customer: dict = stripe.Customer.modify(
                self.stripe_id,
                description=description,
                name=self.firstname,
                email=self.email,
                phone=self.phone,
            )
            Customer.sync_from_stripe_data(customer)
            return customer.get("id", False)
        except Exception as e:
            logger.error("Error: %s " % e.args)
            return False
