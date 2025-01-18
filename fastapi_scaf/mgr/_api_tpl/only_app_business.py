from pydantic import BaseModel, Field


class GetTplBiz(BaseModel):
    id: str = Field(...)

    async def get(self):
        # TODO: 业务逻辑
        pass
