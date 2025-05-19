from django.contrib import admin
from .models import Post, PostEditHistory

admin.site.register(Post)

admin.site.register(PostEditHistory)
