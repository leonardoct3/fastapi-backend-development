from datetime import timedelta
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from app.config.config import security_settings

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET)


def generate_url_safe_token(data: dict, salt: str | None = None) -> str:
    return _serializer.dumps(data, salt=salt)


def decode_url_safe_token(
    token: str,
    salt: str | None = None,
    expiry: timedelta | None = None,
) -> dict:
    try:
        return _serializer.loads(
            token,
            salt=salt,
            max_age=expiry.total_seconds() if expiry else None,
        )
    except (BadSignature, SignatureExpired):
        return None
