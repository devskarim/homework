from django.contrib import admin
from api.models import User, UserConfirmation, Post, Comments, Media

admin.site.register([UserConfirmation, User, Post, Comments, Media])