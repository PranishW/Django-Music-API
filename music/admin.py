from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from music.models import ExtendedUser,Song,Album,Playlist,Follow,LikedSong,LikedAlbum
# Register your models here.
class ExUserInline(admin.StackedInline):
    model = ExtendedUser
    can_delete = False
    verbose_name_plural = 'extendeduser'

class UserAdmin(BaseUserAdmin):
    inlines = [ExUserInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Playlist)
admin.site.register(Follow)
admin.site.register(LikedSong)
admin.site.register(LikedAlbum)

