from datetime import datetime, timedelta, timezone
from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.models import EmailLoginCode


def generate_2fa_code():
    code = ''
    for i in range(4):
        code += str(randint(0, 9))
    return code


def request_login_code(email):
    code = generate_2fa_code()
    EmailLoginCode.objects.create(
        email=email,
        code=code,
    )

    send_mail(
        subject="Login code",
        message=code,
        from_email=None,
        recipient_list=[email]
    )

def check_login_code(email, code):
    db_code = EmailLoginCode.objects.filter(email=email, is_used=False).order_by('-created_at').first()
    if db_code is not None:
        if db_code.code == code:
            print(code)
            if datetime.now(timezone.utc) - db_code.created_at < timedelta(minutes=5) and db_code.attempts < 3:
                db_code.is_used = True
                db_code.save()
                return True
            else:
                db_code.is_used = True
                db_code.save()

        db_code.attempts += 1
        db_code.save()
    return False

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }