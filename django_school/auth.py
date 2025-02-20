from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                # Allow login regardless of approval status
                # The view will handle redirecting based on approval
                return user
        except UserModel.DoesNotExist:
            return None
        return None

    def user_can_authenticate(self, user):
        """
        Allow all users to authenticate, even if not approved.
        The view will handle redirecting users based on their approval status.
        """
        return True  # Allow all users to authenticate 