import logging

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from accounts import serializers
from accounts.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


class UserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Регистрация",
        operation_description="Регистриация пользователя",
        tags=["Аккаунты"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError:
            return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)


class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error("Error: %s" % e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Профиль",
        operation_description="",
        tags=["Аккаунты"]
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Профиль",
        operation_description="",
        tags=["Аккаунты"]
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Профиль",
        operation_description="",
        tags=["Аккаунты"]
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Профиль",
        operation_description="",
        tags=["Аккаунты"]
    )
    def get_object(self):
        return self.request.user
