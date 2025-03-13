from django.shortcuts import render
from django.http import JsonResponse
import openai
import os
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup

# Set your OpenAI API key

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

    # Implement your logic to fetch influencer data from Instagram
    # For demonstration, we'll return a mock response
    influencer_data = {
        'username': username,
        'followers': 12345,
        'posts': 67,
        'bio': 'This is a mock bio for the influencer.'
    }
    return JsonResponse(influencer_data)