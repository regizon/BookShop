import logging
import time
from collections import defaultdict

security_logger = logging.getLogger('security_logger')

_WINDOW = 300   # seconds (5 minutes)
_THRESHOLD = 5  # log warning when attempts exceed this value

_ip_attempts: dict[str, list[float]] = defaultdict(list)
_email_attempts: dict[str, list[float]] = defaultdict(list)


def _prune(timestamps: list[float], now: float) -> list[float]:
    cutoff = now - _WINDOW
    return [t for t in timestamps if t > cutoff]


def record_failed_attempt(ip: str, email: str) -> None:
    """Record one failed login attempt and emit security warnings when thresholds are crossed."""
    now = time.time()

    _ip_attempts[ip] = _prune(_ip_attempts[ip], now)
    _ip_attempts[ip].append(now)

    _email_attempts[email] = _prune(_email_attempts[email], now)
    _email_attempts[email].append(now)

    ip_count = len(_ip_attempts[ip])
    email_count = len(_email_attempts[email])

    if ip_count > _THRESHOLD:
        security_logger.warning(
            'BRUTE FORCE — IP: %s | attempts: %d | window: %ds',
            ip,
            ip_count,
            _WINDOW,
        )

    if email_count > _THRESHOLD:
        security_logger.warning(
            'BRUTE FORCE — email: %s | attempts: %d | window: %ds',
            email,
            email_count,
            _WINDOW,
        )
