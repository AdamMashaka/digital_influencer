from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Influencer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    instagram_handle = models.CharField(max_length=100)
    followers = models.IntegerField()

    def __str__(self):
        return self.name  
    
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    dedicated_to = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Question for {self.event.title} by {self.user.username}'
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)  # Ensure unique email addresses
    subscribed_at = models.DateTimeField(auto_now_add=True)  # Automatically store the subscription time

    def __str__(self):
        return self.email


# Create your models here.
