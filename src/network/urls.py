
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.FollowPosts.as_view(), name="following-page"),
    path("liked", views.liked_posts, name="liked-posts"),
    path('likedapi', views.likes_api, name="likedposts-api"),
    path("profile/<int:pk>", views.ProfilePage.as_view(), name="profile-page"),
    path("edit/<int:pk>", views.EditPost.as_view(), name="edit-post"),
    path("like/<int:pk>", views.like_view, name="like_api"),
    path("unlike/<int:pk>", views.unlike_view, name="unlike_api")
]
