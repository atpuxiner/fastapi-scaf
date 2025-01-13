from pydantic import BaseModel


class GetTplBiz(BaseModel):
    id: str

    async def get(self):
        # TODO: 业务逻辑
        pass
