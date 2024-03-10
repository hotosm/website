from django.urls import path

from utils.views import set_language

app_name = "utils"

urlpatterns = [
    path("set_language/", set_language, name="set_language"),
]
