from sqlalchemy import (
    select,
    func,
    update as update_,
    delete as delete_,
)


async def format_all(
        rows,
        fields: list[str],
) -> list[dict]:
    if not rows:
        return list()
    return [dict(zip(fields, row)) for row in rows]


async def format_one(
        row,
        fields: list[str],
) -> dict:
    if not row:
        return dict()
    return dict(zip(fields, row))


async def model_dict(
        model,
        fields: list[str] = None,
) -> dict:
    if not model:
        return dict()
    if not fields:
        fields = [field.name for field in model.__table__.columns]
    return {field: getattr(model, field) for field in fields}


async def query_one(
        session,
        model,
        fields: list[str] = None,
        filter_by: dict = None,
) -> dict:
    if not fields:
        fields = [field.name for field in model.__table__.columns]
    query = select(*[getattr(model, field) for field in fields]).select_from(model)
    if filter_by:
        query = query.filter_by(**filter_by)
    result = await session.execute(query)
    return await format_one(result.fetchone(), fields)


async def query_all(
        session,
        model,
        fields: list[str] = None,
        filter_by: dict = None,
        page: int = None,
        size: int = None,
) -> list[dict]:
    if not fields:
        fields = [field.name for field in model.__table__.columns]
    query = select(*[getattr(model, field) for field in fields]).select_from(model)
    if filter_by:
        query = query.filter_by(**filter_by)
    if page and size:
        query = query.offset((page - 1) * size).limit(size)
    result = await session.execute(query)
    return await format_all(result.fetchall(), fields)


async def query_total(
        session,
        model,
        filter_by: dict = None,
) -> int:
    query = select(func.count()).select_from(model)
    if filter_by:
        query = query.filter_by(**filter_by)
    result = await session.execute(query)
    return result.scalar()


async def create(
        session,
        model,
        data: dict,
        filter_by: dict = None,
) -> int:
    try:
        if filter_by:
            result = await query_one(session, model, filter_by=filter_by)
            if result:
                return 0
        stmt = model(**data)
        session.add(stmt)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return stmt.id


async def update(
        session,
        model,
        data: dict,
        filter_by: dict,
        is_exclude_none: bool = True,
) -> tuple[int, str]:
    try:
        if is_exclude_none:
            data = {k: v for k, v in data.items() if v is not None}
        stmt = (
            update_(model)
            .values(**data)
            .returning(model.id)
        )
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        result = await session.execute(stmt)
        count = len(result.fetchall())
        await session.commit()
        if count > 0:
            msg = f"更新成功"
        else:
            msg = "未找到匹配的记录"
    except Exception:
        await session.rollback()
        raise
    return count, msg


async def delete(
        session,
        model,
        filter_by: dict,
) -> tuple[int, str]:
    try:
        stmt = (
            delete_(model)
            .returning(model.id)
        )
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        result = await session.execute(stmt)
        count = len(result.fetchall())
        await session.commit()
        if count > 0:
            msg = f"删除成功"
        else:
            msg = "未找到匹配的记录"
    except Exception:
        await session.rollback()
        raise
    return count, msg
