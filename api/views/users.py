from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate

from api.models import User, VERIFIED, DONE, NEW
from api.serializers import EmailSerializer, CodeSerializer, SignUpSerializer, LoginSerializer
from api.utilits import send_code, CustomResponse


class SendCodeApiView(APIView):
    serializer_class = EmailSerializer

    @swagger_auto_schema(request_body=EmailSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user, _ = User.objects.get_or_create(email=email)
        code = user.create_code()

        refresh = RefreshToken.for_user(user)

        send_code(email=user.email, code=code)

        return CustomResponse.succes(
            message="Verification code sent",
            data=str(refresh.access_token)
        )


class CodeVerifyApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code")

        if self.verify_user(user, code):
            return CustomResponse.succes(message="User verified!")

        return CustomResponse.error(message="Code expired or incorrect.")

    def verify_user(self, user, code):
        confirmation = user.confirmations.order_by("-created_at").first()

        if confirmation and not confirmation.is_expired() and confirmation.code == code:
            user.status = VERIFIED
            user.save()
            return True

        return False


class ResendCodeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if self.resend_code(user):
            return CustomResponse.succes(message="Verification code resent")

        return CustomResponse.error(
            message="You already have an active code or something went wrong."
        )

    def resend_code(self, user):
        confirmation = user.confirmations.order_by("-created_at").first()

        if confirmation and confirmation.is_expired() and user.status == NEW:
            code = user.create_code()
            send_code(user.email, code=code)
            return True

        return False


class SignUpApiView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.status != VERIFIED:
            return CustomResponse.error(message="User is not verified yet")

        user.username = serializer.validated_data.get("username")
        user.phone = serializer.validated_data.get("phone")
        user.first_name = serializer.validated_data.get("first_name")
        user.last_name = serializer.validated_data.get("last_name", "N/A")
        user.set_password(serializer.validated_data.get("password"))
        user.status = DONE
        user.save()

        data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone
        }

        return CustomResponse.succes(
            message="User registered successfully",
            data=data
        )

class LoginApiView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            return CustomResponse.error(
                message="Invalid username or password"
                  )

        if user is not None:
            return CustomResponse.succes(
                message="User logged succesfully",
                data=user.token()
            )

        return CustomResponse.error(
            message="user not found"
        )