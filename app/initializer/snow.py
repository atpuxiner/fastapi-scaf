from toollib.guid import SnowFlake


def init_snow(
        worker_id: int,
        datacenter_id: int,
) -> SnowFlake:  # 建议：采用服务的方式调用api获取
    return SnowFlake(worker_id=worker_id, datacenter_id=datacenter_id, to_str=True)
