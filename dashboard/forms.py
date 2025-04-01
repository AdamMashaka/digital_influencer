from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'category', 'project_cost', 'priority', 'start_date', 'end_date', 'assigned_to', 'description']

    def clean(self):
        # Additional custom validation can be placed here
        return super().clean()
    
    
# events/forms.py


class EventForm(forms.ModelForm):
   class Meta:
        model = Calender_event
        fields = ['title', 'start', 'end', 'description']