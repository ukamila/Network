from django.contrib import admin

from .models import User, Post, Follower
# Register your models here.

class NewUserAdmin(admin.ModelAdmin):
    user_display = ("id", "username", "password")

admin.site.register(User, NewUserAdmin)
admin.site.register(Post)
admin.site.register(Follower)
