from django.urls import path
from django.views.i18n import set_language

app_name = "utils"
urlpatterns = [
    # ... your other urls
    path("setlang/", set_language, name="set_language"),
]
