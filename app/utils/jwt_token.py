from datetime import datetime, timedelta, timezone
import uuid
import jwt
from fastapi import HTTPException, status
from app.config.config import security_settings
from jwt import ExpiredSignatureError, PyJWTError

def generate_access_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    return jwt.encode(
            payload={
                **data,
                "jti": str(uuid.uuid4()),
                "exp": datetime.now(timezone.utc) + expiry
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET
        )

def decode_access_token(token: str):
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    except PyJWTError:
        return None
