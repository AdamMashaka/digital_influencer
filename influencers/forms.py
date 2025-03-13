from .models import Event
from django import forms
from .models import Question 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, help_text='Enter phone number in +255 format')
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
    
    
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        
                    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
        
        
class MeetingLinkForm(forms.Form):
    link = forms.URLField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def save(self):
        # save the meeting link and password
        pass        
        
        