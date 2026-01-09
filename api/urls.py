from django.urls import path 
from rest_framework.routers import DefaultRouter

from api.views import SendCodeApiView, CodeVerifyApiView, ResendCodeApiView, SignUpApiView, LoginAPIView, PostViewApiView

router = DefaultRouter()
router.register(r"posts", PostViewApiView)

urlpatterns = [
	path('send-code/', SendCodeApiView.as_view()), 
	path('code-verify/', CodeVerifyApiView.as_view()),
	path('code-resend/', ResendCodeApiView.as_view()),
	path('signup/', SignUpApiView.as_view()),
	path('Login/', LoginAPIView.as_view()),
]

urlpatterns  += router.urls 