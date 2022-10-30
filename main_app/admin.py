from django.contrib import admin
from .models import Listing, Photo
from .models import Comment
# Register your models here.

admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Photo)
