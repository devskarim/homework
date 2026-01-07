from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.models import User 
from api.utilits import send_code	
from api.serializers import EmailSerializer


class SendCodeApiView(APIView):
    serializer_class = EmailSerializer
    
    @swagger_auto_schema(request_body=EmailSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        user, _ = User.objects.get_or_create(email=email)

        code = user.create_code()

        send_code(user=user, email=email, code=code)

        return Response({
            "status": True,
            "message": "Verification code sent successfully"
        }, status=200)
