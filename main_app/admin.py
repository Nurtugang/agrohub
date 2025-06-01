from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    Thing, NewsCategory, News, Newsletter,
    ServiceProvider, ServiceCategory, Service, ServiceImage, ServiceRequest
)


@admin.register(Thing)
class ThingAdmin(TranslationAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    
    # Show all language fields in the form
    fields = ('name_ru', 'name_kk', 'name_en', 'description_ru', 'description_kk', 'description_en')
    
    class Meta:
        model = Thing
        

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
   list_display = ('name', 'slug')
   prepopulated_fields = {'slug': ('name',)}
   search_fields = ('name',)


@admin.register(News)
class NewsAdmin(TranslationAdmin):
   list_display = ('title', 'category', 'created_at', 'is_published')
   list_filter = ('category', 'is_published', 'created_at')
   search_fields = ('title', 'content')
   prepopulated_fields = {'slug': ('title',)} if hasattr(News, 'slug') else {}
   date_hierarchy = 'created_at'
   list_editable = ('is_published',)
   
   fieldsets = (
       (None, {
           'fields': ('title', 'content', 'image', 'category', 'is_published')
       }),
   )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


# Service models
@admin.register(ServiceProvider)
class ServiceProviderAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'order', 'is_active')
        }),
    )


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 100px;">'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'provider', 'price', 'currency', 'is_active', 'created_at')
    list_filter = ('category', 'provider', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_active')
    date_hierarchy = 'created_at'
    inlines = [ServiceImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'provider')
        }),
        ('Описание', {
            'fields': ('short_description', 'description', 'duration')
        }),
        ('Цена', {
            'fields': ('price', 'currency')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('service', 'alt_text', 'is_primary', 'order', 'image_preview')
    list_filter = ('is_primary', 'service__category')
    search_fields = ('service__name', 'alt_text')
    list_editable = ('is_primary', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 100px;">'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'client_name', 'client_email', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service__category', 'service__provider')
    search_fields = ('client_name', 'client_email', 'service__name')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Услуга', {
            'fields': ('service',)
        }),
        ('Клиент', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Заявка', {
            'fields': ('message', 'status')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} заявок отмечены как подтвержденные.')
    mark_as_confirmed.short_description = "Отметить как подтвержденные"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} заявок отмечены как завершенные.')
    mark_as_completed.short_description = "Отметить как завершенные"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} заявок отмечены как отмененные.')
    mark_as_cancelled.short_description = "Отметить как отмененные"