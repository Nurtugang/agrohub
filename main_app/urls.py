from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('things/', views.things_list, name='things_list'),
    
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('lab/', views.lab, name='lab'),
    path('agrotehnopark/', views.agrotehnopark, name='agrotehnopark'),
    path('engeneering_center/', views.engeneering_center, name='engeneering_center'),
    
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    path('services/', views.services_list, name='services_list'),
    path('services/request/', views.service_request, name='service_request'),
    path('services/cart-request/', views.cart_service_request, name='cart_service_request'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    path('courses/', views.courses_list, name='courses_list'),
    path('course/application/', views.course_application, name='course_application'), 
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    
    path('projects/', views.projects_catalog, name='projects_catalog'),
    path('project/<slug:slug>/', views.project_detail, name='project'),
    
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
]