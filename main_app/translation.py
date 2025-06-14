from modeltranslation.translator import TranslationOptions, register
from .models import *


@register(Thing)
class ThingTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    
@register(Expert)
class ExpertTranslationOptions(TranslationOptions):
   fields = ('name', 'bio')

@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
   fields = ('name',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
   fields = ('title', 'content', 'short_description')


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
    

@register(CourseCategory)
class CourseCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'short_description')


@register(Instructor)
class InstructorTranslationOptions(TranslationOptions):
    fields = ('name', 'title', 'bio')


@register(CourseModule)
class CourseModuleTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(CourseTopic)
class CourseTopicTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(CourseReview)
class CourseReviewTranslationOptions(TranslationOptions):
    fields = ('reviewer_name', 'comment')
    

@register(ProjectDirection)
class ProjectDirectionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProjectStatus)
class ProjectStatusTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'implementation_period')


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):
    fields = ('caption',)


@register(ProjectTeamMember)
class ProjectTeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'position', 'bio')
    
@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'availability', 'delivery_time')