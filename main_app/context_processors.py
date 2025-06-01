from django.utils.translation import gettext as _
from django.conf import settings


def language_context(request):
    """Context processor for language switching and menu options"""
    
    menu_options = {
        '/': _('menu_home'),
        '/things/': _('menu_things'),
        '/about/': _('menu_about'),
    }
    
    return {
        'menu_options': menu_options,
        'current_path': request.path,
        'available_languages': settings.LANGUAGES,
    }