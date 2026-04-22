

import datetime
import uuid

from pydantic import BaseModel, Field, EmailStr



class UserRegisterRequest(BaseModel): 
    name: str = Field(min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Robert Kubica",
                "email": "rkubica@najszybszywokolicy.com",
                "password": "russell1234"
            }
        }
    }

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserModel(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
