
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("likepost", views.likepost, name="likepost"),
    path("dislikepost", views.dislikepost, name="dislikepost"),
    path("editPost", views.editPost, name="editPost"),
    path("saveEditedPost", views.saveEditedPost, name="saveEditedPost"),
    path("profile/<str:username>/<str:username2>", views.showprofile, name="profilepage"),
    path("follow/<str:wannafollow>", views.follow, name="follow"),
    path("unfollow/<str:wannaunfollow>", views.unfollow, name="unfollow"),
    path("followingPosts", views.followingPosts, name="followingPosts")
    #path("editPost/<int:postid>/<str:postuser>/<str:user>", views.editPost, name="editPost")
]
