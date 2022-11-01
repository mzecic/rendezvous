from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.description}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'listing_id': self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.user} - {self.location}'


class Comment(models.Model):
    content = models.TextField('Write a comment',max_length=300)
    date = models.DateField('Comment Date')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.content} - {self.listing}'

class Photo(models.Model):
  url = models.CharField(max_length=200)
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for listing_id: {self.listing_id} @{self.url}"
