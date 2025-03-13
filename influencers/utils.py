import africastalking
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Event

# Initialize the SDK
username = "simalert"
api_key = "atsk_94aa349740a23ddbd524123b63ab70914b65b92300d6f05c191dd43581dd01d642aa0a22"
africastalking.initialize(username, api_key)

# Get the SMS service
sms = africastalking.SMS

def send_sms(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print(response)
    except Exception as e:
        print(f"Error sending SMS: {e}")

def user_is_superuser_or_cabinet_member(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        if event_id:
            event = get_object_or_404(Event, id=event_id)
            if request.user.is_superuser or request.user in event.cabinet_members.all():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        else:
            return HttpResponseForbidden("Event ID is required.")
    return _wrapped_view