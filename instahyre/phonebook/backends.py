# backends.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class MobileNumberBackend(BaseBackend):
    def authenticate(self, request, mobile=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(mobile=mobile)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None
