from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import User


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for custom user objects."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name"]
        read_only_fields = ("email",)


class CustomRegisterSerializer(RegisterSerializer):
    """Serializer for custom registeration."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, max_length=150)

    def __init__(self, *args, **kwargs):
        self.fields.pop('password1')
        self.fields.pop('password2')
        self.fields.pop('username')
        super().__init__(*args, **kwargs)

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'full_name': self.validated_data.get('full_name', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )

        user.full_name = self.cleaned_data['full_name']
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomLoginSerializer(LoginSerializer):
    """Serializer for login."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
