import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, BigInteger, Integer, String
from toollib.utils import now2timestamp

from app.datatype import DeclBase
from app.initializer import g


class User(DeclBase):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, default=g.snow.gen_uid, comment="主键")
    phone = Column(String(15), unique=True, index=True, nullable=False, comment="手机号")
    password = Column(String(128), nullable=True, comment="密码")
    jwt_key = Column(String(128), nullable=True, comment="jwtKey")
    name = Column(String(50), nullable=True, comment="名称")
    age = Column(Integer, nullable=True, comment="年龄")
    gender = Column(Integer, nullable=True, comment="性别")
    created_at = Column(BigInteger, default=now2timestamp, comment="创建时间")
    updated_at = Column(BigInteger, onupdate=now2timestamp, default=now2timestamp, comment="更新时间")


class GetUserReq(BaseModel):
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


class GetUserListReq(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10

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


class CreateUserReq(BaseModel):
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$')
    password: str = Field(...)
    name: str = Field("", pattern=r'^[\u4e00-\u9fffA-Za-z]{1,50}$')
    age: int = Field(0, ge=0, le=200)
    gender: int = Field(0, ge=0, le=2)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{6,20}$', v):
            raise ValueError("密码必须包含至少一个字母和一个数字，长度为6到20个字符")
        return v

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


class UpdateUserReq(BaseModel):
    name: str = Field(None, pattern=r'^[\u4e00-\u9fffA-Za-z]{1,50}$')
    age: int = Field(None, ge=0, le=200)
    gender: int = Field(None, ge=0, le=2)


class DeleteUserReq(BaseModel):
    pass


class LoginUserReq(BaseModel):
    phone: str
    password: str


class TokenUserReq(BaseModel):
    user_id: int
