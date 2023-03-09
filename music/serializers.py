from rest_framework import serializers
from music.models import ExtendedUser,Song,Album,Playlist,Follow,LikedSong,LikedAlbum
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')

class ExtendedUserSerializer(serializers.ModelSerializer):
    # specify model and fields
    user = UserSerializer()
    class Meta:
        model = ExtendedUser
        fields = ('user','name','phone','age','gender')

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('album','artist','genre','year')

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('sname','album','artist','genre','year')

class PlaylistSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    sname = SongSerializer()
    class Meta:
        model = Playlist
        fields = ('username','playlist_name','sname')

class FollowSerializer(serializers.ModelSerializer):
    following = serializers.StringRelatedField()
    class Meta:
        model = Follow
        fields = ('username','following')

class LikedSongSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    sname =  serializers.StringRelatedField()
    class Meta:
        model = LikedSong
        fields = ('username','sname')

class LikedAlbumSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    album =  serializers.StringRelatedField()
    class Meta:
        model = LikedAlbum
        fields = ('username','album')