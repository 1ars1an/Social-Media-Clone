from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View

from .models import User, Post
from .forms import CreatePost

class Index(View): #displays all posts, allows user to create post if authenticated
    def get(self, request):
        all_posts = Post.objects.all()
        return render(request, "network/index.html", {'posts': all_posts, 'form': CreatePost()})

    def post(self, request):
        form = CreatePost(request.POST)
        all_posts = Post.objects.all()
        if form.is_valid():
            content = form.cleaned_data['content']
            user_post = Post(creator=request.user, content=content)
            user_post.save()
            return redirect(reverse('index'))
        else:
            print(form.errors)
            return render(request, "network/index.html", {'posts': all_posts, 'form': CreatePost(), 'message': form.errors})

class ProfilePage(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        posts = user.posts.all()
        context = {'user': user, 'posts': posts}
        return render(request, "network/profile.html", context)

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
    


