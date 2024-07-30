from app.business.base import BaseBiz
from app.datatype.tpl import (
    GetTplReq,
)


class GetTplBiz(GetTplReq, BaseBiz):

    async def get(self):
        pass
