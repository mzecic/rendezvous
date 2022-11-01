from django.contrib import admin
from .models import Listing, Photo, Comment, Profile
# Register your models here.

admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Photo)
admin.site.register(Profile)
