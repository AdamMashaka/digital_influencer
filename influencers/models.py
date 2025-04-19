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
    
class  Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    passkey = models.CharField(max_length=8, default='DEFAULT_PASSKEY')
    role = models.CharField(max_length=50, default='Participant')  
    checked_in = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[('registered', 'Registered'), ('missed', 'Missed'), ('success', 'Success')], default='registered')
    checkin_link = models.CharField(max_length=32, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Tanzania')
    area_of_interest = models.CharField(max_length=100, default='General')
    language = models.CharField(max_length=100, default='English')
    communication = models.CharField(max_length=100, default='Email,Phone')
    attended = models.BooleanField(default=False)  
    allow_marketing = models.BooleanField(default=True)
    
    def __str__(self): 
        return f"{self.name} - {self.event.title}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15)
    area_of_interest = models.CharField(max_length=100, default='General') 
    subsector_of_interest = models.CharField(max_length=100, blank=True, null=True)
    citizenship = models.CharField(max_length=100)
    other_citizenship = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    other_designation = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Tanzania')
    company = models.CharField(max_length=100, blank=True, null=True) 
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    passkey = models.CharField(max_length=6, blank=True, null=True)
    communication = models.CharField(max_length=100, default='Email,Phone')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.username = self.user.username
        self.email = self.user.email
        super().save(*args, **kwargs)
    
    
    


# Create your models here.
