from pydantic import BaseModel
from sqlalchemy import Column, BigInteger, String

from app.datatype import DeclBase, filter_fields
from app.initializer import g


class Tpl(DeclBase):
    __tablename__ = "tpl"

    id = Column(BigInteger, primary_key=True, default=g.snow.gen_uid, comment="主键")
    name = Column(String(50), nullable=True, comment="名称")


class GetTplMdl(BaseModel):
    id: int
    # #
    name: str = None

    @classmethod
    def response_fields(cls):
        return filter_fields(
            cls,
            exclude=[]
        )
