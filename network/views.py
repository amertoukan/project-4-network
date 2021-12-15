import json
import logging


from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse



from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt



from .models import User, Follow, Post 
logger = logging.getLogger(__name__)


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    # p = Paginator(posts, 3)
    # page = 1
    # if request.GET.get('page'):
    #     page = request.GET.get('page')

    # current_page = p.page(page)
    return render(request, "network/index.html", {
        # "current_page": current_page, 
        # "page_number": page, 
        # "page_range": p.page_range,
        "following": False, 
        "posts": posts
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
        poster = request.user
        content = request.POST["content"]
        Post.objects.create(poster=poster, content=content)
        return HttpResponseRedirect(reverse("index"))

def profile(request, user): 
    profile_to_view = User.objects.get(username = user)
    posts = Post.objects.filter(poster=profile_to_view).order_by('id').reverse()
    followers = Follow.objects.filter(following=profile_to_view).count()
    following = Follow.objects.filter(user=profile_to_view).count()

    try: 
        is_following = Follow.objects.get(user = request.user, following = profile_to_view)
    except (ObjectDoesNotExist, TypeError): 
        is_following = None
    return render (request, "network/profile.html", {
        "profile": profile_to_view, 
        "followers": followers, 
        "following": following, 
        "is_following": is_following, 
        "posts": posts
    })


def follow(request, user): 
    user_to_follow = User.objects.get(username=user)
    current_user = request.user
    try: 
        existing_follow_object = Follow.objects.get(user=request.user, following = user_to_follow)
    except ObjectDoesNotExist: 
        existing_follow_object = None
    if existing_follow_object: 
        existing_follow_object.delete()
    else: 
        follow_object = Follow(user=current_user, following=user_to_follow)
        follow_object.save()
    return HttpResponseRedirect(reverse("profile", args=[user]))


def following(request): 
    following_objects = Follow.objects.filter(user = request.user)
    users_following = [follow.following for follow in following_objects]
    all_posts = Post.objects.all().order_by('id').reverse()
    following_posts = [post for post in all_posts if post.poster in users_following]
    return render(request, "network/index.html", {
        "following": True, 
        "following_posts": following_posts
    })


@csrf_exempt
def edit (request, post_id): 
    post = Post.objects.get(pk = post_id)
    if request.user == post.poster: 
        if request.method == "PUT": 
            data = json.loads(request.body)
            content_to_save = data ["content"]
            if post.content != content_to_save: 
                post.content = content_to_save
                post.save() 
            return HttpResponse(status=200)
        else: 
            return render (request, "network/error.html")
@csrf_exempt
def like (request, post_id): 
    post_object = Post.objects.get(pk=post_id)
    current_user = request.user 
    if current_user not in post_object.likes.all(): 
        post_object.likes.add(current_user)
        post_object.save()
    else: 
        post_object.likes.add(current_user)
        post_object.save() 
    return JsonResponse({"likes": post_object.likes.count()})