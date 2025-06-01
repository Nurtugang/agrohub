from modeltranslation.translator import TranslationOptions, register
from .models import Thing, NewsCategory, News, Newsletter, ServiceProvider, ServiceCategory, Service


@register(Thing)
class ThingTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    

@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
   fields = ('name',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
   fields = ('title', 'content')


@register(Newsletter)
class NewsletterTranslationOptions(TranslationOptions):
   fields = ()
   
   
@register(ServiceProvider)
class ServiceProviderTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ServiceCategory)
class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'duration')