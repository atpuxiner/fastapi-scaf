from app.datatype.user import (
    User,
    UserDetailMdl,
    UserListMdl,
    UserCreateMdl,
    UserUpdateMdl,
    UserDeleteMdl,
    UserLoginMdl,
    UserTokenMdl,
)
from app.initializer import g
from app.utils import auth, db_async


class UserDetailBiz(UserDetailMdl):

    async def detail(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                fields=self.response_fields(),
                filter_by={"id": self.id},
            )
            return data


class UserListBiz(UserListMdl):

    async def lst(self):
        async with g.db_async_session() as session:
            data = await db_async.query_all(
                session=session,
                model=User,
                fields=self.response_fields(),
                page=self.page,
                size=self.size,
            )
            total = await db_async.query_total(session, User)
            return data, total


class UserCreateBiz(UserCreateMdl):

    async def create(self):
        async with g.db_async_session() as session:
            return await db_async.create(
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


class UserUpdateBiz(UserUpdateMdl):

    async def update(self, user_id: str):
        async with g.db_async_session() as session:
            return await db_async.update(
                session=session,
                model=User,
                data=self.model_dump(),
                filter_by={"id": user_id},
            )


class UserDeleteBiz(UserDeleteMdl):

    @staticmethod
    async def delete(user_id: str):
        async with g.db_async_session() as session:
            return await db_async.delete(
                session=session,
                model=User,
                filter_by={"id": user_id},
            )


class UserLoginBiz(UserLoginMdl):

    async def login(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                filter_by={"phone": self.phone},
            )
            if not data or not auth.verify_password(self.password, data.get("password")):
                return None
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
                exp_minutes=24 * 60 * 30,
            )
            # 更新jwt_key
            await db_async.update(
                session=session,
                model=User,
                data={"jwt_key": new_jwt_key},
                filter_by={"phone": self.phone},
            )
            return token


class UserTokenBiz(UserTokenMdl):

    async def token(self):
        async with g.db_async_session() as session:
            data = await db_async.query_one(
                session=session,
                model=User,
                filter_by={"id": self.id},
            )
            if not data:
                return None
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
                exp_minutes=self.exp_minutes,
            )
            # 更新jwt_key
            await db_async.update(
                session=session,
                model=User,
                data={"jwt_key": new_jwt_key},
                filter_by={"id": self.id},
            )
            return token
