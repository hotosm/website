from django.shortcuts import redirect
from django.utils import translation


def set_language(request):
    language_code = request.GET.get("language_code")
    translation.activate(language_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = language_code
    return redirect(request.META.get("HTTP_REFERER"))
