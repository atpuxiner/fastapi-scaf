from pydantic import BaseModel
from sqlalchemy import Column, BigInteger, String

from app.datatype import DeclBase
from app.initializer import g


class Tpl(DeclBase):
    __tablename__ = "tpl"

    id = Column(BigInteger, primary_key=True, default=g.snow.gen_uid, comment="主键")
    name = Column(String(50), nullable=True, comment="名称")


class GetTplReq(BaseModel):
    tpl_id: int

    @property
    def fields(self):
        return [
            "id",
            "name",
        ]
