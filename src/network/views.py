from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View

from .models import User, Post, SocialSystem, LikeSystem
from .forms import CreatePost

def get_likes(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        return list(user.liked.all().values_list('post', flat=True))
    else:
        return []

class Index(View): #displays all posts, allows user to create post if authenticated
    def get(self, request):
        all_posts = Post.objects.all()
        paginator = Paginator(all_posts, 10)
        pg_num = request.GET.get('page', 1)
        pg_obj = paginator.get_page(pg_num)
        whoYouLiked = get_likes(request)
        return render(request, "network/index.html", {'pg_posts': pg_obj, 'form': CreatePost(), 'e_form': CreatePost(), 'whoYouLiked': whoYouLiked})

    def post(self, request):
        form = CreatePost(request.POST)
        all_posts = Post.objects.all()
        paginator = Paginator(all_posts, 10)
        pg_num = request.GET.get('page', 1)
        pg_obj = paginator.get_page(pg_num)
        whoYouLiked = get_likes(request)
        if form.is_valid():
            content = form.cleaned_data['content']
            user_post = Post(creator=request.user, content=content)
            user_post.save()
            return redirect(reverse('index'))
        else:
            return render(request, "network/index.html", {'pg_posts': pg_obj, 'form': CreatePost(), 'message': form.errors, 'e_form': CreatePost(), 'whoYouLiked': whoYouLiked})

class ProfilePage(LoginRequiredMixin, View):
    def follow_check(self, request, user):
        if len(user.followers.values().filter(user=request.user.id)):
            isFollowing = True
        else:
            isFollowing = False
        return isFollowing
    
    def display(self, request, user):
        paginator = Paginator(user.posts.all(), 5)
        pg_num = request.GET.get('page', 1)
        pg_obj = paginator.get_page(pg_num)
        return pg_obj

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        pg_obj = self.display(request, user)

        following = user.following.values().count()
        followers = user.followers.values().count()
        whoYouLiked = get_likes(request)
        context = {'p_user': user, 'pg_posts': pg_obj, 'following': following, 'followers': followers, 'isFollowing': self.follow_check(request, user), 'e_form': CreatePost(), 'whoYouLiked': whoYouLiked}
        return render(request, "network/profile.html", context)
    
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        f_action = request.POST.get('action')
        if 'Unfollow' in f_action:
            u_obj = user.followers.get(user=request.user)
            u_obj.delete()
        else:
            u_obj = SocialSystem(user=request.user, following_user=user)
            u_obj.save()

        return redirect(reverse_lazy('profile-page', args=[pk]))
    
class FollowPosts(LoginRequiredMixin, View):
    def get(self, request):
        follow_list = request.user.following.all().values_list('following_user', flat=True)
        all_posts = Post.objects.none() #creating empty query set
        for fl in follow_list: #we use union so that we can get a query set combining results of each query set instead of double looping over a queryset of querysets
            all_posts = all_posts.union(Post.objects.filter(creator=fl).order_by()) #remove ordering to avoid sql lite error: Order by not allowed in subqueries of compound statements
        paginator = Paginator(all_posts.order_by('-created'), 10) #add ordering again
        pg_num = request.GET.get('page', 1)
        pg_obj = paginator.get_page(pg_num)
        whoYouLiked = get_likes(request)
        return render(request, "network/following-page.html", {'pg_posts': pg_obj, 'whoYouLiked': whoYouLiked})
    
class EditPost(View):
    def post(self, request, pk):
        u_post = get_object_or_404(Post, id=pk)
        print(u_post)
        if request.user != u_post.creator:
            return redirect(reverse('index'))
        form = CreatePost(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            u_post.content = content
            u_post.save()
            return redirect(reverse('index'))
        else:
            return redirect(reverse('index'))
        
def liked_posts(request):
    whoYouLiked = get_likes(request)
    l_obj = []
    for liked in whoYouLiked:
        print(liked)
        l_obj.append(get_object_or_404(Post, id=liked))
    return render(request, "network/liked-posts.html", {'pg_posts': l_obj, 'whoYouLiked': whoYouLiked})
        
def like_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = get_object_or_404(User, id=request.user.id)
    new_like = LikeSystem(user=user, post=post)
    new_like.save()
    return JsonResponse({'message': 'liked post!'})

def unlike_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = get_object_or_404(User, id=request.user.id)
    LikeSystem.objects.filter(user=user, post=post).delete()
    return JsonResponse({'message': 'unliked post!'})

def likes_api(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        retval = list(user.liked.all().values_list('post', flat=True))
        return JsonResponse({'likeList': retval})
    else:
        return JsonResponse({'likeList': []})

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
    


