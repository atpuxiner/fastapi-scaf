from toollib.guid import SnowFlake


def init_snow(
        worker_id: int,
        datacenter_id: int,
) -> SnowFlake:  # 建议采用服务api的方式获取雪花id
    return SnowFlake(worker_id=worker_id, datacenter_id=datacenter_id)
