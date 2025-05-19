from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import ModelSerializer, CharField, EmailField, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .models import ConsumptionLog
from .serializers import ConsumptionLogSerializer


# ConsumptionLog viewset
class ConsumptionLogViewSet(viewsets.ModelViewSet):
    queryset = ConsumptionLog.objects.all().order_by('-timestamp')
    serializer_class = ConsumptionLogSerializer
    permission_classes = [permissions.IsAuthenticated]


# Serializer for user registration
class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)  # Confirm password field renamed
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user


# Registration API view
class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key,
        }, status=status.HTTP_201_CREATED)


# Custom login view for obtaining auth token
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]


# Password Reset Serializer and View
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build your frontend reset URL (adjust domain accordingly)
        reset_url = f"http://your-frontend-domain/reset-password/{uid}/{token}"

        subject = "Password Reset Requested"
        message = f"Hi {user.username},\n\nYou requested a password reset. Use the link below to reset your password:\n\n{reset_url}\n\nIf you didn't request this, ignore this email."
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'no-reply@example.com'
        send_mail(subject, message, from_email, [email])

        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)


# Password Reset Confirm Serializer and View
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = CharField()
    token = CharField()
    new_password = CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, data['token']):
            raise ValidationError("Invalid or expired token.")

        data['user'] = user
        return data


class PasswordResetConfirmAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
