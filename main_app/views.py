import json
from django.db.models import Q
from django.conf import settings
from django.utils import translation
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from .models import Thing, News, NewsCategory, Newsletter, Service, ServiceProvider, ServiceCategory, ServiceProvider, ServiceRequest
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    """Main page with multilingual content"""
    locale = translation.get_language()
    things = Thing.objects.all()
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    context = {
        'things': things,
        'current_language': locale,
        'latest_news': latest_news,
    }
    return render(request, 'index.html', context)


def things_list(request):
    """List all things with translations"""
    locale = translation.get_language()
    things = Thing.objects.all()
    
    context = {
        'things': things,
        'current_language': locale,
    }
    return render(request, 'things.html', context)


def about(request):
    locale = translation.get_language()
    
    context = {
        'current_language': locale,
    }
    return render(request, 'about.html', context)

def team(request):
    locale = translation.get_language()
    
    context = {
        'current_language': locale,
    }
    return render(request, 'team.html', context)

def lab(request):
    locale = translation.get_language()
    
    context = {
        'current_language': locale,
    }
    return render(request, 'lab.html', context)

def change_language(request, language_code):
    """Change the current language"""
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        request.session[settings.LANGUAGE_SESSION_KEY] = language_code
        translation.activate(language_code)

    # Redirect back to the previous page
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('/')


def news_list(request):
    news = News.objects.filter(is_published=True)
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        news = news.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Фильтр по категории
    category_filter = request.GET.get('category', '')
    if category_filter and category_filter != 'all':
        news = news.filter(category__slug=category_filter)
    
    # Фильтр по периоду
    period_filter = request.GET.get('period', '3months')
    if period_filter == '1month':
        date_from = datetime.now() - timedelta(days=30)
        news = news.filter(created_at__gte=date_from)
    elif period_filter == '3months':
        date_from = datetime.now() - timedelta(days=90)
        news = news.filter(created_at__gte=date_from)
    elif period_filter == '6months':
        date_from = datetime.now() - timedelta(days=180)
        news = news.filter(created_at__gte=date_from)
    elif period_filter == '1year':
        date_from = datetime.now() - timedelta(days=365)
        news = news.filter(created_at__gte=date_from)
    
    # Сортировка
    sort_filter = request.GET.get('sort', 'newest')
    if sort_filter == 'newest':
        news = news.order_by('-created_at')
    elif sort_filter == 'oldest':
        news = news.order_by('created_at')
    elif sort_filter == 'title':
        news = news.order_by('title')
    
    # Пагинация
    paginator = Paginator(news, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Категории для фильтра
    categories = NewsCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'period_filter': period_filter,
        'sort_filter': sort_filter,
    }
    
    return render(request, 'news.html', context)


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_published=True)
    related_news = News.objects.filter(
        category=news.category, 
        is_published=True
    ).exclude(pk=pk)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    
    return render(request, 'news_detail.html', context)


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '')
    
    if not email:
        return JsonResponse({
            'success': False, 
            'message': _('Email адрес обязателен')
        })
    
    newsletter, created = Newsletter.objects.get_or_create(email=email)
    
    if created:
        return JsonResponse({
            'success': True,
            'message': _('Вы успешно подписались на рассылку!')
        })
    else:
        return JsonResponse({
            'success': False,
            'message': _('Этот email уже подписан на рассылку')
        })


def services_list(request):
    """Страница списка услуг"""
    # Фильтры
    provider_filter = request.GET.get('provider', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    # Получаем все активные услуги
    services = Service.objects.filter(is_active=True).select_related('category', 'category__provider')
    
    # Применяем фильтры
    if provider_filter:
        services = services.filter(category__provider__slug=provider_filter)
    
    if category_filter:
        services = services.filter(category__slug=category_filter)
        try:
            selected_category = ServiceCategory.objects.get(slug=category_filter)
            services = services.filter(category__provider=selected_category.provider)
        except ServiceCategory.DoesNotExist:
            pass
    
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(services, 12)  # 12 услуг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Данные для фильтров
    providers = ServiceProvider.objects.filter(is_active=True)
    
    # Категории зависят от выбранного провайдера
    categories = ServiceCategory.objects.filter(is_active=True)
    if provider_filter and provider_filter != 'all':
        categories = categories.filter(provider__slug=provider_filter)
    categories = categories.order_by('order', 'name')
    
    # Текущая активная акция (если есть)
    current_promotion = None
    
    context = {
        'page_obj': page_obj,
        'providers': providers,
        'categories': categories,
        'provider_filter': provider_filter,
        'category_filter': category_filter,
        'search_query': search_query,
        'current_promotion': current_promotion,
    }
    
    return render(request, 'services.html', context)


@require_POST
def cart_service_request(request):
    """Создание заявки на консультацию для нескольких услуг из корзины"""
    try:
        # Получаем данные из формы
        service_ids_json = request.POST.get('service_ids')
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        message = request.POST.get('message', '')
        print(service_ids_json, client_name, client_email, client_phone, message)
        # Валидация данных
        if not all([service_ids_json, client_name, client_email, client_phone]):
            return JsonResponse({
                'success': False,
                'message': 'Заполните все обязательные поля'
            })
        
        # Парсим список ID услуг
        try:
            service_ids = json.loads(service_ids_json)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Ошибка в данных корзины'
            })
        
        # Получаем услуги
        services = Service.objects.filter(id__in=service_ids, is_active=True)
        
        if not services.exists():
            return JsonResponse({
                'success': False,
                'message': 'Выбранные услуги не найдены'
            })
        
        # Создаем заявку
        service_request = ServiceRequest.objects.create(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            message=message
        )
        
        # Добавляем услуги к заявке
        service_request.services.set(services)
        
        # Пересчитываем общую сумму
        service_request.calculate_total()
        
        # Формируем сообщение об успехе
        services_names = [service.name for service in services]
        success_message = f"Заявка на консультацию создана! Услуги: {', '.join(services_names)}. Общая сумма: {service_request.total_price} ₸"
        
        return JsonResponse({
            'success': True,
            'message': success_message,
            'request_id': service_request.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка: {str(e)}'
        })


@require_POST  
def service_request(request):
    """Создание заявки на консультацию для одной услуги (существующая функциональность)"""
    try:
        # Получаем данные из формы
        service_id = request.POST.get('service_id')
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        message = request.POST.get('message', '')
        
        # Валидация данных
        if not all([service_id, client_name, client_email, client_phone]):
            return JsonResponse({
                'success': False,
                'message': 'Заполните все обязательные поля'
            })
        
        # Получаем услугу
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Услуга не найдена'
            })
        
        # Создаем заявку
        service_request = ServiceRequest.objects.create(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            message=message
        )
        
        # Добавляем одну услугу к заявке
        service_request.services.add(service)
        
        # Пересчитываем общую сумму
        service_request.calculate_total()
        
        return JsonResponse({
            'success': True,
            'message': f'Заявка на консультацию по услуге "{service.name}" создана!',
            'request_id': service_request.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка: {str(e)}'
        })
        
          
def service_detail(request, slug):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(slug=slug)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'service_detail.html', context)

def courses(request):
    locale = translation.get_language()
    
    context = {
        'current_language': locale,
    }
    return render(request, 'courses.html', context)

def course(request):
    locale = translation.get_language()
    
    context = {
        'current_language': locale,
    }
    return render(request, 'course.html', context)
