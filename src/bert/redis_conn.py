from redis import Redis


class RedisConnection:
    def conn(self) -> Redis:
        host = "localhost"
        port = 6379
        redis_conn = Redis(host=host, port=port)
        return redis_conn
