from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('things/', views.things_list, name='things_list'),
    
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('lab/', views.lab, name='lab'),
    
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    path('services/', views.services_list, name='services_list'),
    path('services/request/', views.service_request, name='service_request'),
    path('services/cart-request/', views.cart_service_request, name='cart_service_request'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    path('courses/', views.courses, name='courses'),    
    path('course/', views.course, name='course'),    
    
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
]