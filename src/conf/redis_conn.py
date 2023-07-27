import redis

from conf.config_manager import ConfigManager


class RedisConnection:
    def __init__(self):
        self.config = ConfigManager().get_config_file()

    def conn(self) -> redis.Redis:
        host = self.config["cache"]["name"]
        port = self.config["cache"]["port"]
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn
