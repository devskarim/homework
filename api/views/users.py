from rest_framework.views import APIView

from api.utilits import send_code

class SendCode(APIView):

	def post(self, request): 
		serializer = self.serializer_class(data= request.data)
		serializer