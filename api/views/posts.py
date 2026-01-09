from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from api.serializers import PostSerializer, MediaSerializer
from api.models import Post, Comment, Media

@extend_schema(tags=['ForPosts'])
class PostViewApiView(ModelViewSet): 
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def get_permissions(self):
		if self.action == "list": 
			permission_classes  = [IsAuthenticated, ] 
		else: 
			pass