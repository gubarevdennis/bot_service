import pytest
import datetime
from jose import jwt
from app.core.config import settings

@pytest.fixture
def create_test_token():
    def _create_token(sub="test_user", role="user"):
        to_encode = {
            "sub": sub,
            "role": role,
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
        }
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return _create_token