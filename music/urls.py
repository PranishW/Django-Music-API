"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from music import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("users", views.UserViewSet, basename="users")
router.register("albums", views.AlbumViewSet, basename="albums")
router.register("songs", views.SongViewSet, basename="songs")
router.register("playlists", views.MyPlaylistViewSet, basename="my-playlists")
router.register("allplaylists", views.AllPlaylistViewSet, basename="all-playlists")
router.register("following", views.FollowingListViewSet, basename="my-following")
router.register("likedsong", views.LikedSongListViewSet, basename="my-likedsong")
router.register("likedalbum", views.LikedAlbumListViewSet, basename="my-likedalbum")
router.register("alllikedsong", views.AllLikedSongListViewSet, basename="all-likedsong")
router.register("alllikedalbum", views.AllLikedAlbumListViewSet, basename="all-likedalbum")
#router.register("auth/login",obtain_auth_token,basename="create-token")

urlpatterns = [
    path('', include(router.urls))
]
