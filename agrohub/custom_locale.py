from django.middleware.locale import LocaleMiddleware
from django.conf import settings
from django.utils import translation


class CustomLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        if settings.LANGUAGE_SESSION_KEY in request.session:
            translation.activate(request.session[settings.LANGUAGE_SESSION_KEY])
        else:
            translation.activate(settings.LANGUAGE_CODE)