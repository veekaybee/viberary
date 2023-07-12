import redis

from inout.file_reader import get_config_file as conf


class RedisConnection:
    def __init__(self):
        self.config = conf()

    def conn(self) -> redis.Redis:
        host = self.config["cache"]["name"]
        port = self.config["cache"]["port"]
        pool = redis.ConnectionPool(host=host, port=port, db=0, decode_response=True)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn
