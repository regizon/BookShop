from datetime import datetime, timedelta, timezone
from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

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

    print(code)

    send_mail(
        subject="Login code",
        message=code,
        from_email=None,
        recipient_list=[email]
    )

def check_login_code(email, code):
    user = EmailLoginCode.objects.filter(email=email, is_used=False).first()
    if user is not None:
        user = user[0]
        if user.code == code:
            if datetime.now(timezone.utc) - user.created_at < timedelta(minutes=5) and user.attempts < 3:
                user.is_used = True
                user.save()
                return True
            else:
                user.is_used = True
                user.save()

        user.attempts += 1
    return False