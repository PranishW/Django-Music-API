from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ExtendedUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(null=True)
    age = models.IntegerField()
    gender = models.CharField( max_length=50)

    def __str__(self):
        return self.user.get_username()
        
    
    
class Album(models.Model):
    album = models.CharField(primary_key=True,max_length=50)
    artist = models.CharField(max_length=50)
    genre = models.CharField( max_length=50)
    year = models.DateField()

    def __str__(self):
        return self.album

class Song(models.Model):
    sname = models.CharField(max_length=50,null=False)
    album = models.ForeignKey(Album,related_name='songs', on_delete=models.CASCADE)
    artist = models.CharField(max_length=50)
    genre = models.CharField( max_length=50)
    year = models.DateField()

    def __str__(self):
        return self.sname

class Playlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    sname = models.ForeignKey(Song,related_name='song', on_delete=models.CASCADE,null=True) 

    def __str__(self):
        return self.playlist_name

class Follow(models.Model):
    username = models.CharField(max_length=50) # user in username attribute is following the user in following attribute
    following = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class LikedSong(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    sname = models.ForeignKey(Song, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.username) + " Liked Song"

class LikedAlbum(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username) + " Liked Album"