from django.conf import settings
from django.urls import path, include


urlpatterns = [
    #path("moderators/", include("apps.moderators.urls"))
]


if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
