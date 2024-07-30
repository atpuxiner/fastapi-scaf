from sqlmodel import SQLModel, Field
from typing import Optional

from app.api.exception import ParamsError


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    phone: str = Field(index=True, unique=True)
    password: str = Field(default=None)
    jwt_key: str = Field(default=None)
    name: str = Field(default=None)
    age: int = Field(default=None)
    gender: int = Field(default=None)
    created_at: int = Field(default=None)
    updated_at: int = Field(default=None)


class GetUserReq(SQLModel):
    user_id: int

    @property
    def fields(self):
        return [
            "id",
            "phone",
            "name",
            "age",
            "gender",
            "created_at",
            "updated_at",
        ]


class GetUserListReq(SQLModel):
    page: Optional[int] = 1
    size: Optional[int] = 10

    @property
    def offset(self):
        return (self.page - 1) * self.size

    @property
    def fields(self):
        return [
            "id",
            "phone",
            "name",
            "age",
            "gender",
            "created_at",
            "updated_at",
        ]


class CreateUserReq(SQLModel):
    phone: str
    password: str
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = None

    def validate_params(self):
        if self.gender and self.gender not in [1, 2]:
            raise ParamsError("gender is EMUM(1, 2)")

    @property
    def fields(self):
        return [
            "id",
            "phone",
            "name",
            "age",
            "gender",
            "created_at",
            "updated_at",
        ]


class UpdateUserReq(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = None


class DeleteUserReq(SQLModel):
    pass


class LoginUserReq(SQLModel):
    phone: str
    password: str

    @property
    def fields(self):
        return ",".join([
            "id",
            "phone",
            "password",
            "jwt_key",
            "name",
            "age",
            "gender",
        ])


class TokenUserReq(SQLModel):
    user_id: int

    @property
    def fields(self):
        return ",".join([
            "id",
            "phone",
            "name",
            "age",
            "gender",
        ])
