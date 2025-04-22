from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .utils import send_sms 
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from .models import Influencer
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import logging
from .forms import  RegistrationForm,ContactForm, MeetingLinkForm
import json
from django.http import HttpResponse
from .models import Registration, Profile 

logger = logging.getLogger(__name__)


openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    logger.error("Kwibo API key not found in environment variables")
else:
    logger.info(f"Kwibo API key found: {openai_api_key}")


openai.api_key = openai_api_key

@csrf_exempt
def ask_openai(request):
    if request.method == 'POST':
        try:
         
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)

         
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant specializing in providing information exclusively "
                            "about the Kwibo, including it is roles, services, events, "
                            "and other related topics. If a question is unrelated to Kwibo, politely redirect the user "
                            "to focus on TIC or contact +255734989470 for more information. If you are unsure about the answer, kindly direct the user to visit "
                            "our main website at https://starbuzz.ai/ or contact us at 0694021848."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                temperature=0.7,
                max_tokens=150,
            )


            answer = response.choices[0].message.content.strip()
            return JsonResponse({'answer': answer})

        except Exception as e:
            import traceback
            logger.error("Error during kwibo API call: %s", traceback.format_exc())
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


ACCESS_TOKEN = '1002792908415536|DEpcT8fn-E13NsoDF8Ud6PicADQ' 

def home(request):
    return render(request, 'website/index.html') 

def about(request):
    return render(request, 'website/about.html')

def solution(request):
    return render(request, 'website/solution.html')

@csrf_exempt
def ask_bot(request):
    question = request.GET.get('question')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are Kwibobuzz Bot, an expert in influencer marketing and social media. Answer only questions related to influencers and social media."},
                {"role": "user", "content": question}
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()
        return JsonResponse({'response': answer})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
def scrape_starbuzz(request):
    url = "https://starbuzz.ai"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
       
        data = []
        for item in soup.select('.some-css-selector'):  
            data.append(item.get_text(strip=True))
        
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def fetch_influencer(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'No username provided'}, status=400) 

 
    user_search_url = f"https://graph.facebook.com/v18.0/{username}?fields=id,username,profile_picture_url,biography,followers_count,media_count&access_token={ACCESS_TOKEN}"
    
    response = requests.get(user_search_url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch influencer details'}, status=400)

    influencer_data = response.json()

    data = {
        'username': influencer_data.get('username', 'Unknown'),
        'followers': influencer_data.get('followers_count', 0),
        'posts': influencer_data.get('media_count', 0),
        'bio': influencer_data.get('biography', 'No bio available'),
        'image_url': influencer_data.get('profile_picture_url', ''),
    }

    return JsonResponse(data)

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not subject or not message:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                'mashakaadam123gmail.com', 
                ['mashakaadam123@gmail.com'], 
                fail_silently=False,
            )
            return JsonResponse({'success': 'Your message has been sent. Thank you!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



@csrf_exempt
def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)

        try:
            
            send_mail(
                'Newsletter Subscription',
                'Thank you for subscribing to our newsletter!',
                'your-email@example.com',  
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': 'Your subscription request has been sent. Thank you!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'website/signin.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')

            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            login(request, user)
            messages.success(request, 'Registration successful.')

            subject = 'Welcome to Our Platform!'
            html_message = render_to_string('website/emails/congratulations.html', {'user': user, 'current_year': timezone.now().year})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to = user.email

            try:
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                logger.info(f'Welcome email sent to {to}')
            except Exception as e:
                logger.error(f'Error sending email: {e}')
                messages.error(request, 'Registration successful, but there was an error sending the confirmation email.')

            sms_message = "Welcome to our platform! Your registration was successful."
            try:
                send_sms(phone_number, sms_message)
                logger.info(f'Welcome SMS sent to {phone_number}')
            except Exception as e:
                logger.error(f'Error sending SMS: {e}')
                messages.error(request, 'Registration successful, but there was an error sending the welcome SMS.')

            return redirect('welcome')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form}) 



@login_required
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('home')
    else:
        return redirect('home')
    
    
    
def dashboard(request):
    return render(request, 'dashboard/index.html') 

def send_sms(phone_number, message):
    
    pass

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            'tic.events@tic.go.tz',
            ['your-email@example.com'],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse(f'Error sending email: {e}')
    
def welcome(request):
    return render(request, 'website/authentication/general/welcome.html')

@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    registered_events = Registration.objects.filter(user=user).count()
    missed_events = Registration.objects.filter(user=user, status='missed').count()
    success_events = Registration.objects.filter(user=user, status='success').count()
    
    if missed_events > 0:
        success_rate = round((success_events / missed_events) * 100, 1)
    else:
        success_rate = 100.0 if success_events > 0 else 0.0

    profile_fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'country', 'area_of_interest', 'company']
    filled_fields = sum(1 for field in profile_fields if getattr(user, field, None) or getattr(profile, field, None))
    profile_completion = round((filled_fields / len(profile_fields)) * 100, 1)

    
    sectors = profile.area_of_interest.split(',') if profile.area_of_interest else []
    subsectors = profile.subsector_of_interest.split(',') if profile.subsector_of_interest else []

    context = {
        'user': user,
        'profile': profile,
        'registered_events': registered_events,
        'missed_events': missed_events,
        'success_rate': success_rate,
        'profile_completion': profile_completion,
        'sectors': sectors,
        'subsectors': subsectors, 
    }

    return render(request, 'website/profile.html', context)



@login_required
def settingi(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    
    if request.method == 'POST':
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        profile.phone = request.POST.get('phone')
        profile.country = request.POST.get('country')
        profile.language = request.POST.get('language')
        profile.company = request.POST.get('company')
        profile.communication = ','.join(request.POST.getlist('communication'))
        profile.allow_marketing = 'allow_marketing' in request.POST
        profile.area_of_interest = ','.join(request.POST.getlist('area_of_interest'))  # Save as a comma-separated string
        profile.subsector_of_interest = ','.join(request.POST.getlist('subsector_of_interest'))  # Save as a comma-separated string

        user.save() 
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    context = {
        'user': user, 
        'profile': profile, 
    }
    return render(request, 'dashboards/backoffice/account/settings.html', context)

def custom_404(request, exception):
    return render(request, 'website/404.html', status=404)

def custom_403(request, exception):
    return render(request, 'website/403.html', status=403)

def custom_500(request):
    return render(request, 'website/500.html', status=500)

def trigger_error(request):
    raise Exception("This is a test 500 error.") 



 
