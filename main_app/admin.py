from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *


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
    list_display = ('name', 'provider', 'slug', 'order', 'is_active')
    list_filter = ('provider', 'is_active')
    search_fields = ('name', 'provider__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'provider', 'order', 'is_active')
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
    list_display = ('name', 'category', 'get_provider', 'price', 'currency', 'is_active', 'created_at')
    list_filter = ('category__provider', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_active')
    date_hierarchy = 'created_at'
    inlines = [ServiceImageInline]
    
    def get_provider(self, obj):
        return obj.category.provider.name
    get_provider.short_description = 'Provider'
    get_provider.admin_order_field = 'category__provider__name'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category')
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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = ServiceCategory.objects.filter(is_active=True).select_related('provider').order_by('provider__name', 'order', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ('client_name', 'get_services_count', 'get_services_list_short', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'services__category__provider', 'services__category')
    search_fields = ('client_name', 'client_email', 'services__name')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    filter_horizontal = ('services',)  # Удобный виджет для выбора множественных услуг
    
    def get_services_count(self, obj):
        return obj.services.count()
    get_services_count.short_description = 'Количество услуг'
    get_services_count.admin_order_field = 'services__count'
    
    def get_services_list_short(self, obj):
        services = obj.services.all()[:3]  # Показываем только первые 3
        names = [service.name for service in services]
        if obj.services.count() > 3:
            names.append(f"... и еще {obj.services.count() - 3}")
        return ", ".join(names)
    get_services_list_short.short_description = 'Услуги'
    
    fieldsets = (
        ('Услуги', {
            'fields': ('services',)
        }),
        ('Клиент', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Заявка', {
            'fields': ('message', 'status', 'total_price')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Пересчитываем общую сумму после сохранения
        obj.calculate_total()
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled', 'recalculate_totals']
    
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
    
    def recalculate_totals(self, request, queryset):
        updated = 0
        for obj in queryset:
            obj.calculate_total()
            updated += 1
        self.message_user(request, f'Пересчитана общая сумма для {updated} заявок.')
    recalculate_totals.short_description = "Пересчитать общие суммы"
    

@admin.register(CourseCategory)
class CourseCategoryAdmin(TranslationAdmin):
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


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    fields = ('title', 'order')
    show_change_link = True


class CourseTopicInline(admin.TabularInline):
    model = CourseTopic
    extra = 1
    fields = ('title', 'order')


@admin.register(Course)
class CourseAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'price', 'duration_hours', 'is_active', 'is_popular', 'has_discount', 'created_at')
    list_filter = ('category', 'is_active', 'is_popular', 'has_discount', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'is_active', 'is_popular', 'has_discount')
    date_hierarchy = 'created_at'
    inlines = [CourseModuleInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'main_image')
        }),
        ('Описание', {
            'fields': ('short_description', 'description')
        }),
        ('Стоимость и скидки', {
            'fields': ('price', 'discount_percentage', 'has_discount')
        }),
        ('Характеристики курса', {
            'fields': ('duration_hours', 'hours_per_week')
        }),
        ('Преподаватели', {
            'fields': ('instructors',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'is_popular')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            from django.utils.text import slugify
            import uuid
            obj.slug = f"{slugify(obj.title)}-{str(uuid.uuid4())[:8]}"
        super().save_model(request, obj, form, change)


@admin.register(Instructor)
class InstructorAdmin(TranslationAdmin):
    list_display = ('name', 'title', 'get_courses_count')
    search_fields = ('name', 'title', 'bio')
    
    def get_courses_count(self, obj):
        return obj.taught_courses.count()
    get_courses_count.short_description = 'Количество курсов'
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('name', 'title', 'photo')
        }),
        ('Биография', {
            'fields': ('bio',)
        }),
    )


@admin.register(CourseModule)
class CourseModuleAdmin(TranslationAdmin):
    list_display = ('title', 'course', 'order', 'get_topics_count')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    list_editable = ('order',)
    inlines = [CourseTopicInline]
    
    def get_topics_count(self, obj):
        return obj.topics.count()
    get_topics_count.short_description = 'Количество тем'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order')
        }),
    )


@admin.register(CourseTopic)
class CourseTopicAdmin(TranslationAdmin):
    list_display = ('title', 'get_module', 'get_course', 'order')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'module__title', 'module__course__title')
    list_editable = ('order',)
    
    def get_module(self, obj):
        return obj.module.title
    get_module.short_description = 'Модуль'
    get_module.admin_order_field = 'module__title'
    
    def get_course(self, obj):
        return obj.module.course.title
    get_course.short_description = 'Курс'
    get_course.admin_order_field = 'module__course__title'
    
    fieldsets = (
        (None, {
            'fields': ('module', 'title', 'order')
        }),
    )


@admin.register(CourseReview)
class CourseReviewAdmin(TranslationAdmin):
    list_display = ('reviewer_name', 'course', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at', 'course')
    search_fields = ('reviewer_name', 'comment', 'course__title')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Отзыв', {
            'fields': ('course', 'reviewer_name', 'reviewer_photo', 'rating')
        }),
        ('Комментарий', {
            'fields': ('comment',)
        }),
        ('Модерация', {
            'fields': ('is_approved', 'created_at')
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} отзывов одобрено.')
    approve_reviews.short_description = "Одобрить отзывы"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} отзывов отклонено.')
    disapprove_reviews.short_description = "Отклонить отзывы"


@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'course')
    search_fields = ('full_name', 'phone', 'email', 'course__title')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Заявка', {
            'fields': ('course', 'status')
        }),
        ('Контактная информация', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_contacted', 'mark_as_enrolled', 'mark_as_rejected']
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} заявок отмечены как "Связались".')
    mark_as_contacted.short_description = "Отметить как 'Связались'"
    
    def mark_as_enrolled(self, request, queryset):
        updated = queryset.update(status='enrolled')
        self.message_user(request, f'{updated} заявок отмечены как "Записан".')
    mark_as_enrolled.short_description = "Отметить как 'Записан'"
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} заявок отмечены как "Отклонен".')
    mark_as_rejected.short_description = "Отметить как 'Отклонен'"