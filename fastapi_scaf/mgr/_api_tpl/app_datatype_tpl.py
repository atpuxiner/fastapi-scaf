from sqlmodel import SQLModel, Field


class Tpl(SQLModel, table=True):
    __tablename__ = "tpl"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)


class GetTplReq(SQLModel):
    tpl_id: int

    @property
    def fields(self):
        return [
            "id",
            "name",
        ]
