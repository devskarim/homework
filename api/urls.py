from django.urls import path 

from api.views import SendCodeApiView, CodeVerifyApiView, ResendCodeApiView, SignUpApiView, LoginApiView

urlpatterns = [
	path('send-code/', SendCodeApiView.as_view()), 
	path('code-verify/', CodeVerifyApiView.as_view()),
	path('code-resend/', ResendCodeApiView.as_view()),
	path('signup/', SignUpApiView.as_view()),
	path('Login/', LoginApiView.as_view()),
]