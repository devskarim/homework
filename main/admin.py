from django.contrib import admin
from main.models import User, UserConfirmation, Post, Comments, Media

admin.site.register([UserConfirmation, User, Post, Comments, Media])