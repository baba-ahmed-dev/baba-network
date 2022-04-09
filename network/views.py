from hmac import new
from unittest import result

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from platformdirs import user_config_dir
from rest_framework import pagination
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Follow, Like, Post, Profile, User
from .serializers import (CommentSerializer, FollowSerializer, LikeSerializer,
                          PostSerializer, ProfileSerializer, UserSerializer)


def index(request):
    return render(request, "network/index.html")


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
    return HttpResponseRedirect(reverse("login"))


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

# post fbv
@api_view(["GET","POST"])
def show_list(request):
    if request.method == "GET":
        list = Post.objects.all().order_by('-date')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(list, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



@api_view(["GET"])
def show_user_posts(request ,user_posts):
    if request.method == "GET":
        list = Post.objects.filter(user = user_posts).order_by('-date')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(list, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def show_following_posts(request, user_id):
    if request.method == "GET":
        users = Follow.objects.filter(following=user_id)
        ss = []
        for us in users:
            ss.append(us.followed)
        list = Post.objects.filter(user__in = ss).order_by('-date')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(list, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return HttpResponse(status=404)
    

@api_view(["GET","PUT","DELETE"])
def show_post(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
        
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=204)

# coment fbv
@api_view(["GET","POST"])
def comments(request, post_id):
    if request.method == "GET":
        comments = Comment.objects.filter(post=post_id)
        cmnts = Comment.objects.filter(post=post_id).count()
        serializer = CommentSerializer(comments, many=True)
        content = {'counts':cmnts, "comnts":serializer.data}
        return Response(content)

    elif request.method == "POST":
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)

@api_view(["GET","PUT", "DELETE"])
def comment(request, comment_pk):
    try:
        comment = Comment.objects.get(pk = comment_pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        comment.delete()
        return Response(status=204)

        
# Follow fbv
@api_view(["GET","POST"])
def follow(request, user_id):

    if request.method == "GET":
        follows = Follow.objects.filter(following=user_id).count()
        followers = Follow.objects.filter(followed=user_id).count()
        content = {
            'follows':follows,
            'followers':followers
            }
        return Response(content)
    elif request.method == "POST":

            serializer = FollowSerializer(data = request.data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status = 201)
            return Response(serializer.errors, status=400)

        

@api_view(["GET","DELETE"])
def unfollow(request, flwr, flwrd):
    try:
        follow = Follow.objects.get(following=flwr, followed=flwrd)
    except Follow.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = FollowSerializer(follow)
        return Response(serializer.data)

    elif request.method == "DELETE":
        follow.delete()
        return Response(status=204)

# Like fbv
@api_view(["GET","POST"])
def like(request, post_id):
    if request.method == "GET":
        likes = Like.objects.filter(post=post_id).count()
        content = {'Likes':likes}
        return Response(content)

    elif request.method == "POST":
        serializer = LikeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)
@api_view(["GET","DELETE"])
def unlike(request, post_id, user_id):
    try:
        like = Like.objects.get(user=user_id, post=post_id)
    except Like.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    if request.method == "DELETE":
        like.delete()
        return Response(status=204)

# Profile cbv     
class ProfileView(APIView):
    parser_classes = (MultiPartParser,JSONParser,)        
    
    def get_object(request, user_id):
        try:
           prof = Profile.objects.get(user=user_id)
        except Profile.DoesNotExist:
           return HttpResponse(status=404)

    def get(self, request, user_id, format=None):
        prof = Profile.objects.get(user=user_id)
        serializer = ProfileSerializer(prof)
        return Response(serializer.data)
    
    def post(self, request, user_id, format=None):
        prof_user = request.data.get('user')
        try:
            prof = Profile.objects.get(user=prof_user)
        except Profile.DoesNotExist:
            prof = None
        serializer = ProfileSerializer(prof, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)

    
# get user id
@api_view(["GET"])
def get_user_id(request, username):
    try:
        us = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = UserSerializer(us)
        return Response(serializer.data)

# get random users
@api_view(["GET"])
def get_users_random(request, pk):
    if request.method == "GET":
        users = Follow.objects.filter(following=pk)
        clup = []
        me = User.objects.get(id=pk)
        clup.append(me)
        for us in users:
            clup.append(us.followed)
        jokrs = User.objects.exclude(username__in = clup)
        serializer = UserSerializer(jokrs , many=True)
        return Response(serializer.data)
    return HttpResponse(status=404)
