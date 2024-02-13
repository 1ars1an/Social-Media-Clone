from django.contrib import admin

from .models import User, Post, SocialSystem, LikeSystem
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(SocialSystem)
admin.site.register(LikeSystem)
