from toollib.rediser import RedisCli


def init_redis_cli(
        host: str,
        port: int,
        db: int,
        password: str = None,
        max_connections: int = None,
        **kwargs,
) -> RedisCli:
    if not host:
        return RedisCli()
    return RedisCli(
        host=host,
        port=port,
        db=db,
        password=password,
        max_connections=max_connections,
        **kwargs,
    )
