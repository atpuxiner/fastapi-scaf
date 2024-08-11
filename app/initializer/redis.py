from toollib.redis_cli import RedisCli


def init_redis(
        host: str,
        port: int,
        db: int,
        **kwargs,
) -> RedisCli:
    if not host:
        return RedisCli()
    return RedisCli(host=host, port=port, db=db, **kwargs)
