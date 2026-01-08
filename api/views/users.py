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
    
    @swagger_auto_schema(request_body=EmailSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        user, _ = User.objects.get_or_create(email=email)

        code = user.create_code()
        refresh = RefreshToken.for_user(user)

        send_code(user.email, code=code)

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

					code = serializer.validated_data.get('code')
					
					if self.verify_user(user,  code):
							data = {
								"status": True,
								"message": 'User verified!'
								}
					else: 
							data = {
								"status": False,
								"message": 'Code expired or wrong.'
								}
					return Response(data)
							
			def verify_user(self, user, code): 
						confirmation = user.confirmations.order_by('-created_at').first()
						if not confirmation.is_expired()  and confirmation.code == code:
							user.status  = VERIFIED
							user.save()
							return True

class ResendCodeApiView(APIView): 
	permission_classes = [IsAuthenticated, ]

	def post(self, request): 
		user = request.user
		
		if self.resend_code(user): 
			data = {
				"status": True, 
				"messeage": "Vertification code resent"

			}
		else:
			data = {
				"status": False, 
				"messeage": "You have got unexpired code. or Smth wrong."

			}

		return Response(data)
	
	def resend_code(self, user):
		confirmation = user.confirmations.order_by('-created_at').first()
		if confirmation.is_expired() and user.status == NEW:
			code = user.create_code()
			send_code(user.email, code=code)
			return True