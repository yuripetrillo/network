from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import json
from django.core.paginator import Paginator
from django.shortcuts import render


from .models import User, Post, PostLikes, Follow


@login_required
def index(request):
    posts = Post.objects.all()
    liked_posts = []

    for post in posts:
        try:
            liked=PostLikes.objects.get(post=post.id, user=request.user.pk)
            if liked:
                liked_posts.append(post.id)
        except PostLikes.DoesNotExist:
            pass        
        
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
                "username": request.user,
                'page_posts': list(reversed(page_posts.object_list)),
                "pageIterator": range(1,page_posts.paginator.num_pages + 1),
                "likedPosts": liked_posts
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
    

@login_required
def newpost(request):
    if request.method != "POST":
        return render(request, "network/createPost.html", {
                    "username": request.user,
                })
    elif request.method == "POST":
        post = Post(
        user=User.objects.get(username=request.POST.get("user")),
        title=request.POST.get("title"), 
        content=request.POST.get("content"),
        likes=0,
        timestamp=datetime.now()
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def getPostByUser(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        postid = request.POST.get("postid")
        postuser = request.POST.get("postuser")
        user = request.POST.get("username")
        if user == postuser:
            try:
                post = Post.objects.get(user=User.objects.get(username=postuser), id = postid)
                return post
            except Post.DoesNotExist:
                return HttpResponse(status=404), HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse(status=401), HttpResponseRedirect(reverse("index"))
    
@login_required
def likepost(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            post=Post.objects.get(id=request.POST.get("postid"))
            postLike = PostLikes(
                user=request.user,
                post=post)
            postLike.save()
            post.likes += 1
            post.save()
        except PostLikes.DoesNotExist or Post.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse("index"))



@login_required
def dislikepost(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            post=Post.objects.get(id=request.POST.get("postid"))
            postLike = PostLikes.objects.get(user=request.user, post=post)
            postLike.delete()

            if post.likes > 0:
                post.likes -= 1
            post.save()
        except PostLikes.DoesNotExist or Post.DoesNotExist:
            pass  
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def editPost(request):
    if request.method != "POST":
        return HttpResponse(status=500)
    #add control
    post = getPostByUser(request)
    if (post):    
        return HttpResponse(post.content)
    else:
        return HttpResponse(status=404)
    
@login_required
def saveEditedPost(request):
    if request.method != "POST":
        return HttpResponse(status=500)
    #add control
    post = getPostByUser(request)
    if (post):  
        post.content = request.POST.get("content") 
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
    
@login_required
def showprofile(request, username, username2):
    if request.method == "POST":
        return HttpResponse(status=404)
    else:
         try:
            userobj=User.objects.get(username=username)
            userobj2=User.objects.get(username=username2)
            followers=Follow.objects.filter(following=userobj)
            following=Follow.objects.filter(follower=userobj)
            posts=Post.objects.filter(user=userobj)
            checkfollow=Follow.objects.filter(follower=userobj2, following=userobj)
            doFollow=False
            if len(checkfollow) > 0:
                doFollow=True
            return render(request, "network/profile.html", {
                    "user": request.user,
                    "username": username,
                    "following": len(following),
                    "followers": len(followers),
                    "posts": len(posts),
                    "doFollow": doFollow
                })
         except User.DoesNotExist or Follow.DoesNotExist or Post.DoesNotExist:
            return HttpResponse(status=500)
        
@login_required
def follow(request, wannafollow):
    if request.method != "POST":
        return HttpResponse(status=404)
    else:
         try:
            follow = Follow (
                follower=User.objects.get(username=request.POST.get("usernameO")),
                following=User.objects.get(username=wannafollow)
            )
            follow.save()
            return HttpResponseRedirect(reverse("index"))
         except User.DoesNotExist or Follow.DoesNotExist:
            return HttpResponse(status=500)
         
@login_required
def unfollow(request, wannaunfollow):
    if request.method != "POST":
        return HttpResponse(status=404)
    else:
         try:
            userobj=User.objects.get(username=request.POST.get("usernameO"))
            userobj2=User.objects.get(username=wannaunfollow)
            follow = Follow.objects.get(follower=userobj, following=userobj2)
            follow.delete()
            return HttpResponseRedirect(reverse("index"))
         except User.DoesNotExist or Follow.DoesNotExist:
            return HttpResponse(status=500)

@login_required
def followingPosts(request):
    followedUsers = Follow.objects.filter(follower=request.user.pk)
    filteredPosts = []

    for user in followedUsers:
        try:
            posts = Post.objects.all().filter(user=user.following)
            filteredPosts.append(posts)
        except PostLikes.DoesNotExist:
            pass     

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    return render(request, "network/followingPosts.html", {
                "username": request.user,
                'page_posts': list(reversed(page_posts.object_list)),
                "pageIterator": range(1,page_posts.paginator.num_pages + 1),
                "filteredPosts": filteredPosts
            })