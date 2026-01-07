from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import  IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from api.models import User, VERIFIED, DONE,  NEW
from api.utilits import send_code	
from api.serializers import EmailSerializer, CodeSerializer


class SendCodeApiView(APIView):
    serializer_class = EmailSerializer
    
		
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        user, _ = User.objects.get_or_create(email=email)

        code = user.create_code()
        refresh = RefreshToken.for_user(user)

        send_code(user=user, email=email, code=code)

        return Response({
            "status": True,
            "message": "Verification code sent", 
            "token": str(refresh.access_token)
        })
    
class CodeVerifyApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        if self.verify_user(user, code):
            refresh = RefreshToken.for_user(user)

            return Response({
                "status": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response({
            "status": False,
            "message": "Invalid or expired code"
        }, status=400)
