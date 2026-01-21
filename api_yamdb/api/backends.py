from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class ConfirmationCodeBackend(ModelBackend):
    def authenticate(self, request, username=None, confirmation_code=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            # Проверяем код (предположим, он хранится в поле confirmation_code модели User)
            if user.confirmation_code == confirmation_code:
                return user
        except User.DoesNotExist:
            return None