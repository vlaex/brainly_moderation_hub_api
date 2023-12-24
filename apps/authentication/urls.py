from django.urls import path
from .views import auth


app_name = "authentication"

urlpatterns = [
    path("/auth", auth)
]
