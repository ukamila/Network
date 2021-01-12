import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime, timezone
import pytz

from .models import User, Post, Follower
from django.core.paginator import Paginator

def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
    else:
        liked_posts = []
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        username = request.user 
        body = request.POST['body']
        date = datetime.utcnow().replace(tzinfo=pytz.utc)
        newPage = Post(owner=username, text=body, timestamp=date)
        newPage.save()
        return HttpResponseRedirect(reverse("index"))

def following(request):
    current_user = request.user
    i_am_following = Follower.objects.filter(following=current_user).values_list("followed", flat=True)
    posts = Post.objects.filter(owner__in=i_am_following)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
    else:
        liked_posts = []
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts" :liked_posts
    })

def profile(request, profile):
    profile = User.objects.get(username=profile)
    posts = Post.objects.filter(owner=profile)
    posts = posts.order_by("-timestamp").all()
    followers = Follower.objects.filter(followed=profile)
    followers = len(followers)
    following = Follower.objects.filter(following=profile)
    following = len(following)
    is_following = False
    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
    else:
        liked_posts = []
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if profile != user:
            if len(Follower.objects.filter(following=user).filter( followed=profile))>0:
                is_following = True
            else:
                is_following = False
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile":profile,
        "page_obj": page_obj,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "liked_posts": liked_posts
    })

def follow(request, profile):
    user = User.objects.get(username=request.user)
    profile = User.objects.get(username=profile)
    if len(Follower.objects.filter(following=user).filter( followed=profile))>0:
            Follower.objects.filter(following=user).filter( followed=profile).delete()
    else:
        newFollower = Follower(following=user, followed=profile)
        newFollower.save()
    return HttpResponseRedirect(reverse("profile", args=(profile,)))

@csrf_exempt
@login_required
def save(request):

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("id", "")
    text = data.get("text", "")

    post = Post.objects.get(pk=post_id)
    post.text = text
    post.save()

    return JsonResponse({"message": "Post was edited successfully."}, status=201)

@csrf_exempt
@login_required
def like(request):

    if request.method == "POST":
    
        data = json.loads(request.body)
        which_id = data.get("post", "")
        post = Post.objects.get(pk=which_id)
        post.likes.add(request.user)
        post.save()
        return JsonResponse({"message":"success"}, status=201)
    
    return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
@login_required
def unlike(request):

    if request.method == "POST":
     
        data = json.loads(request.body)
        which_id = data.get("post", "")
        post = Post.objects.get(pk=which_id)
        post.likes.remove(request.user)
        post.save()
        return JsonResponse({"message": "success"}, status=201)
    
    return JsonResponse({"error": "POST request required."}, status=400)


    

    
    