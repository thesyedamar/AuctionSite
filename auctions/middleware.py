from django.utils import translation
from django.conf import settings

class ForceActivateLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to get language from session, then cookie, then default
        language = request.session.get('django_language') or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) or settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = language
        response = self.get_response(request)
        translation.deactivate()
        return response
