from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from config.settings import API_KEY


class APIKeyAuthentication(BaseAuthentication):
    keyword = "Api-Key"

    def authenticate(self, request):
        api_key = request.headers.get("X-API-KEY") or request.headers.get("Api-Key")
        if not api_key:
            return None

        if api_key != API_KEY:
            raise AuthenticationFailed("Chave da API inválida.")

        return (api_key, api_key)
