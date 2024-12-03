from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from starlette.requests import Request

from app.api.exception import CustomException
from app.api.status import Status
from app.datatype.user import User
from app.initializer import g
from app.utils import db_async
from app.utils.auth import verify_jwt


class JWTUser(BaseModel):
    id: int = None
    phone: str = None
    name: str = None
    age: int = None
    gender: int = None


class JWTAuthorizationCredentials(HTTPAuthorizationCredentials):
    user: JWTUser


class JWTBearer(HTTPBearer):

    async def __call__(
            self, request: Request
    ) -> Optional[JWTAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise CustomException(
                    msg="Not authenticated",
                    status=Status.UNAUTHORIZED_ERROR,
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise CustomException(
                    msg="Invalid authentication credentials",
                    status=Status.UNAUTHORIZED_ERROR,
                )
            else:
                return None
        user = await self.verify_credentials(credentials)
        return JWTAuthorizationCredentials(scheme=scheme, credentials=credentials, user=user)

    @staticmethod
    async def verify_credentials(credentials: str) -> JWTUser:
        playload = verify_jwt(credentials)
        if playload is None:
            raise CustomException(status=Status.UNAUTHORIZED_ERROR)
        # 建议：jwt_key进行redis缓存
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                fields=["jwt_key"],
                filter_by={"id": playload.get("id")}
            )
            if not data:
                raise CustomException(status=Status.UNAUTHORIZED_ERROR)
        # <<< 建议
        verify_jwt(credentials, jwt_key=data.get("jwt_key"))
        return JWTUser(
            id=playload.get("id"),
            phone=playload.get("phone"),
            name=playload.get("name"),
            age=playload.get("age"),
            gender=playload.get("gender"),
        )


def get_current_user(
        credentials: Optional[JWTAuthorizationCredentials] = Depends(JWTBearer(auto_error=True))
) -> JWTUser:
    if not credentials:
        return JWTUser()
    return credentials.user
