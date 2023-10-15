import json
import logging
import os
import uuid

import requests
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from djstripe.fields import StripeIdField
from djstripe.models import Customer

from stripe_gateway.customer import CustomerStripeGateway

logger = logging.getLogger(__name__)


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
        user.picture_url = self.get_picture(username)
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

    def get_picture(self, username):
        url = self.get_source_image(username)

        if url is None:
            return settings.ANONYMOUSE_USER

        try:
            response = requests.get(url)
            name_file = "%s.jpg" % uuid.uuid1()
            image_location_root = os.path.join(settings.MEDIA_USER_PROFILE_ROOT, name_file)
            if response.status_code == 200:
                with open(image_location_root, "wb") as f:
                    f.write(response.content)
                return os.path.join(settings.MEDIA_USER_PROFILE_URL, name_file)

            return settings.ANONYMOUSE_USER
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return settings.ANONYMOUSE_USER
        except Exception as e:
            logger.error(e)
            return settings.ANONYMOUSE_USER

    @staticmethod
    def get_source_image(username):
        r = requests.get(
            settings.INSTA_IMAGE_API % username
        )
        try:
            response = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            return None
        return response["graphql"]["user"]["profile_pic_url_hd"]


class User(AbstractBaseUser, PermissionsMixin, CustomerStripeGateway):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    picture_url = models.TextField(null=True, blank=True, default="/static/images/anonymous_user.png")

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
            self.create_user_stripe()
        elif self.stripe_user:
            self.update_stripe_customer()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.delete_stripe_customer():
            super().delete(*args, **kwargs)
