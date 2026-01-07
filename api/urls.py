from django.urls import path 

from api.views import SendCodeApiView, CodeVerifyApiView

urlpatterns = [
	path('send-code/', SendCodeApiView.as_view()), 
	path('code-verify/', CodeVerifyApiView.as_view()),
]