import re

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, BigInteger, Integer, String
from toollib.utils import now2timestamp

from app.datatype import DeclBase, filter_fields
from app.initializer import g


class User(DeclBase):
    __tablename__ = "user"

    id = Column(String(20), primary_key=True, default=g.snow.gen_uid, comment="主键")
    phone = Column(String(15), unique=True, index=True, nullable=False, comment="手机号")
    password = Column(String(128), nullable=True, comment="密码")
    jwt_key = Column(String(128), nullable=True, comment="jwtKey")
    name = Column(String(50), nullable=True, comment="名称")
    age = Column(Integer, nullable=True, comment="年龄")
    gender = Column(Integer, nullable=True, comment="性别")
    created_at = Column(BigInteger, default=now2timestamp, comment="创建时间")
    updated_at = Column(BigInteger, onupdate=now2timestamp, default=now2timestamp, comment="更新时间")


class GetUserMdl(BaseModel):
    id: str
    # #
    phone: str = None
    name: str = None
    age: int = None
    gender: int = None
    created_at: int = None
    updated_at: int = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[]
        )


class GetUserListMdl(BaseModel):
    page: int = 1
    size: int = 10
    # #
    id: str = None
    phone: str = None
    name: str = None
    age: int = None
    gender: int = None
    created_at: int = None
    updated_at: int = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[
                "page",
                "size",
            ]
        )


class CreateUserMdl(BaseModel):
    phone: str = Field(..., pattern=r'^1[3-9]\d{9}$')
    password: str = Field(...)
    name: str = Field("", pattern=r'^[\u4e00-\u9fffA-Za-z0-9_\-.]{1,50}$')
    age: int = Field(0, ge=0, le=200)
    gender: int = Field(0, ge=0, le=2)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)\S{6,20}$', v):
            raise ValueError("密码必须包含至少一个字母和一个数字，长度为6到20的非空白字符")
        return v


class UpdateUserMdl(BaseModel):
    name: str = Field(None, pattern=r'^[\u4e00-\u9fffA-Za-z0-9_\-.]{1,50}$')
    age: int = Field(None, ge=0, le=200)
    gender: int = Field(None, ge=0, le=2)


class DeleteUserMdl(BaseModel):
    pass


class LoginUserMdl(BaseModel):
    phone: str
    password: str


class TokenUserMdl(BaseModel):
    id: str
    exp_minutes: int = 24 * 60 * 30,
