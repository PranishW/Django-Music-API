from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from music.models import ExtendedUser,Song,Album,Playlist,Follow,LikedSong,LikedAlbum
from django.contrib.auth.models import User
from music.serializers import ExtendedUserSerializer,UserSerializer,SongSerializer,AlbumSerializer,PlaylistSerializer,FollowSerializer,LikedSongSerializer,LikedAlbumSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
#users = User.objects.all()
#for user in users:
    #token = Token.objects.get_or_create(user = user)
    #print(token)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = ExtendedUserSerializer
    def get_queryset(self):
        users = ExtendedUser.objects.all()
        return users

    def create(self, request, *args, **kwargs):
        user_data = JSONParser().parse(request)
        new_user = User.objects.create_user(user_data['user']['username'],user_data['user']['email'],user_data['user']['password'])
        new_user.save()
        new_extended_user = ExtendedUser.objects.create(user = new_user,name = user_data['name'],phone = user_data['phone'],
                            age = user_data['age'],gender = user_data['gender'])
        new_extended_user.save()
        #token = Token.objects.get_or_create(user = new_user)
        #print(token)
        serializer = ExtendedUserSerializer(new_extended_user)
        return JsonResponse(serializer.data,status=200)
        
        

class AlbumViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album', 'genre','year']
    def get_queryset(self):
        albums = Album.objects.all()
        return albums
    
    def create(self, request, *args, **kwargs):
        album_data = JSONParser().parse(request)
        new_album = Album.objects.create(album = album_data['album'],artist = album_data['artist'],genre = album_data['genre'],
                            year = album_data['year'])
        new_album.save()
        serializer = AlbumSerializer(new_album)
        return JsonResponse(serializer.data,status=200)


class SongViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    serializer_class = SongSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album', 'genre','year']
    def get_queryset(self):
        songs = Song.objects.all()
        return songs
    
    def create(self, request, *args, **kwargs):
        song_data = JSONParser().parse(request)
        new_song = Song.objects.create(sname = song_data['sname'],album = Album.objects.get(album=song_data["album"]),artist = song_data['artist'],
                        genre = song_data['genre'],year = song_data['year'])
        new_song.save()
        serializer = SongSerializer(new_song)
        return JsonResponse(serializer.data,status=200)

class MyPlaylistViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['playlist_name','sname__album', 'sname__genre','sname__year']
    def get_queryset(self):
        playlists = Playlist.objects.filter(username = self.request.user)
        return playlists

    def create(self, request, *args, **kwargs):
        playlist_data = JSONParser().parse(request)
        try:
            Playlist.objects.get(username = request.user,playlist_name=playlist_data['playlist_name'],sname = Song.objects.get(sname=playlist_data["sname"]))
            error = {"error":"Song already exists in this Playlist"}
            return JsonResponse(error,status=400)
        except ObjectDoesNotExist:
            new_playlist = Playlist.objects.create(username = request.user,playlist_name = playlist_data['playlist_name'],
                            sname = Song.objects.get(sname=playlist_data["sname"]))
            new_playlist.save()
            serializer = PlaylistSerializer(new_playlist)
            return JsonResponse(serializer.data,status=200)

    def delete(self, request, *args, **kwargs): # to delete a song from your playlist
        playlist_data = JSONParser().parse(request)
        try:
            Playlist.objects.get(username = request.user,playlist_name=playlist_data['playlist_name'],sname = Song.objects.get(sname=playlist_data["sname"]))
            playlist = Playlist.objects.get(username = request.user,playlist_name=playlist_data['playlist_name'],sname = Song.objects.get(sname=playlist_data["sname"]))
            rem_playlist = playlist.delete()
            success = {"success":"Playlist Song deleted successfully"}
            return JsonResponse(success,status=200)
        except ObjectDoesNotExist:
            error = {"error":"Song does not exist in this Playlist"}
            return JsonResponse(error,status=400)

class AllPlaylistViewSet(viewsets.ModelViewSet): #to get all playlists 
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['playlist_name','sname__album', 'sname__genre','sname__year']
    def get_queryset(self):
        playlists = Playlist.objects.all()
        return playlists

    def delete(self, request, *args, **kwargs):
        playlist_data = JSONParser().parse(request)
        try:
            Playlist.objects.get(username = request.user,playlist_name=playlist_data['playlist_name'])
            playlist = Playlist.objects.get(username = request.user,playlist_name=playlist_data['playlist_name'])
            rem_playlist = playlist.delete()
            success = {"success":"Playlist deleted successfully"}
            return JsonResponse(success,status=200)
        except ObjectDoesNotExist:
            error = {"error":"Playlist does not exist"}
            return JsonResponse(error,status=400)


class FollowingListViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    def get_queryset(self):
        username = Follow.objects.filter(username = self.request.user)
        return username

    def create(self, request, *args, **kwargs):
        following_data = JSONParser().parse(request)
        try:
            Follow.objects.get(username=request.user,following =User.objects.get(username = following_data["following"]) )
            error = {"error":"You are already following this user"}
            return JsonResponse(error,status=400)
        except ObjectDoesNotExist:
            new_follow = Follow.objects.create(username = request.user.username,following = User.objects.get(username=following_data["following"]))
            new_follow.save()
            serializer = FollowSerializer(new_follow)
            return JsonResponse(serializer.data,status=200)
        

class LikedSongListViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedSongSerializer
    def get_queryset(self):
        likedsong = LikedSong.objects.filter(username = self.request.user)
        return likedsong

    def create(self, request, *args, **kwargs):
        like_song_data = JSONParser().parse(request)
        try:
            LikedSong.objects.get(username=request.user,sname=Song.objects.get(sname=like_song_data["sname"]))
            error = {"error":"Cannot Like a song twice"}
            return JsonResponse(error,status=400)
        except ObjectDoesNotExist:
            new_like = LikedSong.objects.create(username = request.user,sname = Song.objects.get(sname=like_song_data["sname"]))
            new_like.save()
            serializer = LikedSongSerializer(new_like)
            return JsonResponse(serializer.data,status=200)

class LikedAlbumListViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedAlbumSerializer
    def get_queryset(self):
        likedalbum = LikedAlbum.objects.filter(username = self.request.user)
        return likedalbum

    def create(self, request, *args, **kwargs):
        like_album_data = JSONParser().parse(request)
        try:
            LikedAlbum.objects.get(username=request.user,album=Album.objects.get(album=like_album_data["album"]))
            error = {"error":"Cannot Like an album twice"}
            return JsonResponse(error,status=400)
        except ObjectDoesNotExist:
            new_like = LikedAlbum.objects.create(username = request.user,album = Album.objects.get(album=like_album_data["album"]))
            new_like.save()
            serializer = LikedAlbumSerializer(new_like)
            return JsonResponse(serializer.data,status=200)
        
class AllLikedSongListViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedSongSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sname']
    def get_queryset(self):
        likedsong = LikedSong.objects.all()
        return likedsong

class AllLikedAlbumListViewSet(viewsets.ModelViewSet):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikedAlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album']
    def get_queryset(self):
        likedalbum = LikedAlbum.objects.all()
        return likedalbum
