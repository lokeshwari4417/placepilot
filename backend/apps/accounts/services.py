"""
Business logic for account management, kept out of views so it stays
testable and reusable (e.g. from management commands or Celery tasks).
"""
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User


class PasswordResetService:
    @staticmethod
    def generate_reset_token(user: User) -> tuple[str, str]:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uid, token

    @staticmethod
    def send_reset_email(user: User, uid: str, token: str) -> None:
        # Placeholder: wire up to an email backend (SES/SendGrid) later.
        # Kept as a separate method so the send mechanism can change
        # without touching token-generation logic or the view.
        pass
