from sqlalchemy import text, select
from toollib.utils import now2timestamp

from app.business.base import BaseBiz
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
from app.utils import auth


class GetUserBiz(GetUserReq, BaseBiz):

    async def get(self):
        async with g.db_async() as db:
            result = await db.execute(
                statement=text(f"select {', '.join(self.fields)} from user where id = :id"),
                params={"id": self.user_id},
            )
            row = result.first()
            data = self.format_one(row, result.keys())
            return data


class GetUserListBiz(GetUserListReq, BaseBiz):

    async def get_list(self):
        async with g.db_async() as db:
            result = await db.execute(
                statement=text(f"select {', '.join(self.fields)} from user limit :size offset :offset"),
                params={"size": self.size, "offset": self.offset},
            )
            rows = result.fetchall()
            data = self.format_all(rows, result.keys())
            total = 0
            if rows:
                result = await db.execute(text("select count(*) from user"))
                total = result.scalar_one()
            return data, total


class CreateUserBiz(CreateUserReq):

    async def create(self):
        curr_timestamp = now2timestamp()
        new_user = User(
            id=g.snow.gen_uid(),
            name=self.name,
            phone=self.phone,
            age=self.age,
            gender=self.gender,
            password=auth.hash_password(self.password),
            jwt_key=auth.gen_jwt_key(),
            created_at=curr_timestamp,
            updated_at=curr_timestamp,
        )
        async with g.db_async() as db:
            statement = select(User).where(User.phone == self.phone)
            result = await db.execute(statement)
            if result.scalar_one_or_none():
                return False
            db.add(new_user)
            await db.commit()
            return new_user.model_dump(include=self.fields)


class UpdateUserBiz(UpdateUserReq):

    async def update(self, user_id: int):
        async with g.db_async() as db:
            statement = select(User).where(User.id == user_id)
            result = await db.execute(statement)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            update_data = {
                "name": self.name,
                "age": self.age,
                "gender": self.gender,
                "updated_at": now2timestamp(),
            }
            for key, value in update_data.items():
                if value is not None:
                    setattr(user, key, value)
            db.add(user)
            await db.commit()
            return True


class DeleteUserBiz(DeleteUserReq):

    async def delete(self, user_id: int):
        async with g.db_async() as db:
            statement = select(User).where(User.id == user_id)
            result = await db.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                return False
            await db.delete(user)
            await db.commit()
            return True


class LoginUserBiz(LoginUserReq, BaseBiz):

    async def login(self):
        async with g.db_async() as db:
            statement = select(User).where(User.phone == self.phone)
            result = await db.execute(statement)
            user = result.scalar_one_or_none()
            if not user or not auth.verify_password(self.password, user.password):
                return None, "用户名或密码错误"
            new_jwt_key = auth.gen_jwt_key()
            token = auth.gen_jwt(
                payload={
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "age": user.age,
                    "gender": user.gender,
                },
                jwt_key=new_jwt_key,
            )
            user.jwt_key = new_jwt_key
            db.add(user)
            await db.commit()
            return token, ""


class TokenUserBiz(TokenUserReq, BaseBiz):

    async def token(self):
        async with g.db_async() as db:
            statement = select(User).where(User.id == self.user_id)
            result = await db.execute(statement)
            user = result.scalar_one_or_none()
            if not user:
                return None, "用户不存在"
            new_jwt_key = auth.gen_jwt_key()
            token = auth.gen_jwt(
                payload={
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "age": user.age,
                    "gender": user.gender,
                },
                jwt_key=new_jwt_key,
            )
            user.jwt_key = new_jwt_key
            db.add(user)
            await db.commit()
            return token, ""
