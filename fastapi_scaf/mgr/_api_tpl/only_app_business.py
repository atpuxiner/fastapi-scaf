from pydantic import BaseModel


class GetTplBiz(BaseModel):
    id: int

    async def get(self):
        # TODO: 业务逻辑
        pass
