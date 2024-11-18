from app.datatype.user import (
    User,
    GetUserReq,
    GetUserListReq,
    CreateUserReq,
    UpdateUserReq,
    DeleteUserReq,
    LoginUserReq,
    TokenUserReq,
)
from app.initializer import g
from app.utils import auth, db_async


class GetUserBiz(GetUserReq):

    async def get(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                fields=self.fields,
                filter_by={"id": self.user_id},
            )
            return data


class GetUserListBiz(GetUserListReq):

    async def get_list(self):
        async with g.db_async_session() as session:
            data = await db_async.query_all(
                session=session,
                model=User,
                fields=self.fields,
                page=self.page,
                size=self.size,
            )
            total = await db_async.query_total(session, User)
            return data, total


class CreateUserBiz(CreateUserReq):

    async def create(self):
        async with g.db_async_session() as session:
            id_ = await db_async.create(
                session=session,
                model=User,
                data={
                    "name": self.name,
                    "phone": self.phone,
                    "age": self.age,
                    "gender": self.gender,
                    "password": auth.hash_password(self.password),
                    "jwt_key": auth.gen_jwt_key(),
                },
                filter_by={"phone": self.phone},
            )
            return id_


class UpdateUserBiz(UpdateUserReq):

    async def update(self, user_id: int):
        async with g.db_async_session() as session:
            count, msg = await db_async.update(
                session=session,
                model=User,
                data=self.model_dump(),
                filter_by={"id": user_id},
            )
            return count, msg


class DeleteUserBiz(DeleteUserReq):

    @staticmethod
    async def delete(user_id: int):
        async with g.db_async_session() as session:
            count, msg = await db_async.delete(
                session=session,
                model=User,
                filter_by={"id": user_id},
            )
            return count, msg


class LoginUserBiz(LoginUserReq):

    async def login(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                filter_by={"phone": self.phone},
            )
            if not data or not auth.verify_password(self.password, data.get("password")):
                return None, "用户名或密码错误"
            new_jwt_key = auth.gen_jwt_key()
            token = auth.gen_jwt(
                payload={
                    "id": data.get("id"),
                    "phone": data.get("phone"),
                    "name": data.get("name"),
                    "age": data.get("age"),
                    "gender": data.get("gender"),
                },
                jwt_key=new_jwt_key,
            )
            # 更新jwt_key
            await db_async.update(
                session=session,
                model=User,
                data={"jwt_key": new_jwt_key},
                filter_by={"phone": self.phone},
            )
            return token, ""


class TokenUserBiz(TokenUserReq):

    async def token(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                filter_by={"id": self.user_id},
            )
            if not data:
                return None, "用户不存在"
            new_jwt_key = auth.gen_jwt_key()
            token = auth.gen_jwt(
                payload={
                    "id": data.get("id"),
                    "phone": data.get("phone"),
                    "name": data.get("name"),
                    "age": data.get("age"),
                    "gender": data.get("gender"),
                },
                jwt_key=new_jwt_key,
            )
            # 更新jwt_key
            await db_async.update(
                session=session,
                model=User,
                data={"jwt_key": new_jwt_key},
                filter_by={"id": self.user_id},
            )
            return token, ""
