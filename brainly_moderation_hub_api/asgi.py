import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brainly_moderation_hub_api.settings")

application = get_asgi_application()
