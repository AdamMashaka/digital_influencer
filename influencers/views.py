from django.shortcuts import render
from django.http import JsonResponse
import openai
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from django.core.mail import send_mail


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
        
        # Example: Extracting some data from the website
        data = []
        for item in soup.select('.some-css-selector'):  # Update the CSS selector based on the actual website structure
            data.append(item.get_text(strip=True))
        
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def fetch_influencer(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'No username provided'}, status=400)

    # Step 1: Get the user ID from username
    user_search_url = f"https://graph.facebook.com/v18.0/{username}?fields=id,username,profile_picture_url,biography,followers_count,media_count&access_token={ACCESS_TOKEN}"
    
    response = requests.get(user_search_url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch influencer details'}, status=400)

    influencer_data = response.json()

    # Step 2: Return Influencer Data
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
                'your-email@example.com',  # Replace with your email
                ['recipient@example.com'],  # Replace with the recipient's email
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
            # Here you can add the email to your newsletter list
            # For demonstration, we'll just send a confirmation email
            send_mail(
                'Newsletter Subscription',
                'Thank you for subscribing to our newsletter!',
                'your-email@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': 'Your subscription request has been sent. Thank you!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def login_view (request):
    return render(request, 'website/login.html')