from redis import Redis


class RedisConnection:
    def conn(self) -> Redis:
        host = "redis"
        port = 6379
        redis_conn = Redis(host=host, port=port, decode_responses=True)
        return redis_conn
