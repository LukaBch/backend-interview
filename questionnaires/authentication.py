from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from .models import ExpiringToken

class ExpiringTokenAuthentication(TokenAuthentication):
    model = ExpiringToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.has_expired():
            token.delete()
            raise AuthenticationFailed('Token has expired.')
        return token.questionnaire.user, token
