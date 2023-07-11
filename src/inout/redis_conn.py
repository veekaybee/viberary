import redis

from inout.file_reader import get_config_file as conf


class RedisConnection:
    def __init__(self):
        self.config = conf()

    def conn(self) -> redis.Redis:
        host = self.conf["cache"]["name"]
        port = self.conf["cache"]["port"]
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn
