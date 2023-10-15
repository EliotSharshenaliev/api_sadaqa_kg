from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "firstname",
            "lastname",
            "username",
            "phone",
            "email",
            "created_at",
            "stripe_user",
            "picture_url"
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.values("email"))]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.values("username"))]
    )
    phone = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", "username", "email", "password", "confirm_password", "phone")


class UserLoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for authenticating users with email and password.
    """

    def validate(self, data):
        validated_data = super().validate(data)
        self.user.check_user_in_stripe()
        return validated_data
