from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), 
    path('solution/', views.solution, name='solution'),
    path('ask-bot/', views.ask_bot, name='ask_bot'),
    path('fetch-influencer/', views.fetch_influencer, name='fetch_influencer'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('login/', views.login_view, name='login'),
]