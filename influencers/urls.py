from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), 
    path('solution/', views.solution, name='solution'),
    path('ask-bot/', views.ask_bot, name='ask_bot'),
    path('fetch-influencer/', views.fetch_influencer, name='fetch_influencer'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register, name='signup'), 
    path('send-sms/', views.send_sms, name='send_sms'), 
    path('ask-openai/', views.ask_openai, name='ask_openai'),
    path('welcome/', views.welcome, name='welcome'), 
    path('settingi/', views.settingi, name='settingi'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 