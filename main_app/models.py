from django.db import models

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.title} - {self.description}'
