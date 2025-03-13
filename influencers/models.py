from django.db import models

class Influencer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    instagram_handle = models.CharField(max_length=100)
    followers = models.IntegerField()

    def __str__(self):
        return self.name

# Create your models here.
