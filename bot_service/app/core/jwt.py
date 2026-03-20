# bot_service/app/core/jwt.py
from jose import jwt, JWTError
from app.core.config import settings

def decode_and_validate(token: str) -> dict:
    try:
        # decode сам проверит подпись и время жизни (exp)
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        if "sub" not in payload:
            raise ValueError("Token missing sub")
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")