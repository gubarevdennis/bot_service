# auth_service/app/schemas/user.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    # Позволяет Pydantic работать с объектами SQLAlchemy
    model_config = ConfigDict(from_attributes=True)