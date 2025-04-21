from pydantic import BaseModel, Field


class tplDetailBiz(BaseModel):
    id: str = Field(...)

    async def detail(self):
        # TODO: 业务逻辑
        pass
