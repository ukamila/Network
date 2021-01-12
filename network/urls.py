
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("follow/<str:profile>", views.follow, name="follow"),

    #API Routes
    path("save", views.save, name="save"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
]
