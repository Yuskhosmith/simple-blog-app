from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Post, User
from .forms import PostForm

# Create your views here.

def index(request):
    posts = Post.objects.all()

    ctx = {'posts': posts}
    return render(request, 'posts/index.html', ctx)


def post(request, id):
    post = Post.objects.get(id=id)
    ctx = {'post': post}
    return render(request, 'posts/post.html', ctx)


@login_required(login_url='login')
def create_post(request):
    if request.POST:
        form_data = PostForm(request.POST)
        if form_data.is_valid():
            form = form_data.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponseRedirect('post/' + str(form.id))
    
    form = PostForm()
    ctx = {'form': form}
    return render(request, 'posts/createpost.html', ctx)

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
            return render(request, "posts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "posts/login.html")


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
            return render(request, "posts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "posts/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "posts/register.html")
