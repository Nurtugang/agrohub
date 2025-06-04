import os
from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile


class Thing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Thing"
        verbose_name_plural = "Things"
        
        
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    category = models.ForeignKey(NewsCategory, related_name='news', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.compress_image(self.image)
        super().save(*args, **kwargs)
    
    def compress_image(self, image):
        img = Image.open(image)
        img = img.convert('RGB')
        
        if img.width > 1200:
            ratio = 1200 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
        
        output = BytesIO()
        img.save(output, format='WebP', quality=85, optimize=True)
        output.seek(0)
        
        name = os.path.splitext(image.name)[0] + '.webp'
        return ContentFile(output.read(), name=name)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']


class Newsletter(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        




class ServiceProvider(models.Model):
    """Поставщик услуг (Агротехнопарк, Инжиниринг центр, Shakarim Lab)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
        ordering = ['name']


class ServiceCategory(models.Model):
    """Категории услуг (анализ крови, почвы, молока и т.д.)"""
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    provider = models.ForeignKey(ServiceProvider, related_name='categories', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']
        unique_together = ['provider', 'slug']


class Service(models.Model):
    """Конкретная услуга"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='KZT')
    
    # Связи
    category = models.ForeignKey(ServiceCategory, related_name='services', on_delete=models.CASCADE)
    
    # Дополнительные поля
    duration = models.CharField(max_length=100, blank=True, help_text="Время выполнения")
    
    # Мета информация
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = f"{slugify(self.name)}-{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['category', 'name']


class ServiceImage(models.Model):
    """Изображения для услуг"""
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.compress_image(self.image)
        super().save(*args, **kwargs)
    
    def compress_image(self, image):
        img = Image.open(image)
        img = img.convert('RGB')
        
        if img.width > 800:
            ratio = 800 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((800, new_height), Image.Resampling.LANCZOS)
        
        output = BytesIO()
        img.save(output, format='WebP', quality=85, optimize=True)
        output.seek(0)
        
        name = os.path.splitext(image.name)[0] + '.webp'
        return ContentFile(output.read(), name=name)
    
    def __str__(self):
        return f"Image for {self.service.name}"
    
    class Meta:
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"
        ordering = ['order']


class ServiceRequest(models.Model):
    """Заявки на услуги - теперь поддерживает множественный выбор"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    # Изменяем связь с услугами на ManyToMany
    services = models.ManyToManyField(Service, related_name='requests')
    
    # Клиентская информация
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    
    # Добавляем общую сумму
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Статус и временные метки
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_total(self):
        """Подсчет общей стоимости заказа"""
        total = sum(service.price for service in self.services.all())
        self.total_price = total
        self.save()
        return total
    
    def get_services_list(self):
        """Получить список названий услуг"""
        return ", ".join([service.name for service in self.services.all()])
    
    def __str__(self):
        services_count = self.services.count()
        if services_count == 1:
            return f"Request for {self.services.first().name} by {self.client_name}"
        else:
            return f"Request for {services_count} services by {self.client_name}"
    
    class Meta:
        verbose_name = "Service Request"
        verbose_name_plural = "Service Requests"
        ordering = ['-created_at']