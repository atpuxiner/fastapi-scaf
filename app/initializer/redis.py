from toollib.redis_cli import RedisCli


def init_redis(
        host: str,
        port: int,
        db: int,
        password: str = None,
        **kwargs,
) -> RedisCli:
    if not host:
        return RedisCli()
    return RedisCli(host=host, port=port, db=db, password=password, **kwargs)
