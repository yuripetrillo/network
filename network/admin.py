from django.contrib import admin

# Register your models here.
from .models import User, Post, PostLikes, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(Follow)


