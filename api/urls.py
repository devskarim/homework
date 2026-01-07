from django.urls import path 

from api.views import SendCodeApiView

urlpatterns = [
	path('send-code/', SendCodeApiView.as_view())
]