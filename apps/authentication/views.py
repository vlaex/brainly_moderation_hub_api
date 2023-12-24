from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.moderators.models import Moderator
from .token_serializers import TokenObtainPairSerializer


@api_view()
def auth(request):
    moderator = Moderator.objects.get(global_id="ru:18076564")

    token = TokenObtainPairSerializer.get_token(moderator)

    return Response(str(token.access_token))
