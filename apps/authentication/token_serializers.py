from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as DefaultTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.moderators.models import Moderator


class TokenObtainPairSerializer(DefaultTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: Moderator) -> RefreshToken:
        token: RefreshToken = super().get_token(user)

        token["market"] = user.market

        return token
