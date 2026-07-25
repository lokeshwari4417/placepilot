"""
Business logic for account management, kept out of views so it stays
testable and reusable (e.g. from management commands or Celery tasks).
"""
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


class PasswordResetService:
    @staticmethod
    def generate_reset_token(user: User) -> tuple[str, str]:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uid, token

    @staticmethod
    def validate_reset_token(uid: str, token: str) -> User | None:
        try:
            user_pk = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_pk)
            if default_token_generator.check_token(user, token):
                return user
        except (User.DoesNotExist, ValueError, TypeError):
            pass
        return None

    @staticmethod
    def send_reset_email(user: User, uid: str, token: str) -> None:
        # Placeholder: wire up to an email backend (SES/SendGrid) later.
        # Kept as a separate method so the send mechanism can change
        # without touching token-generation logic or the view.
        pass
