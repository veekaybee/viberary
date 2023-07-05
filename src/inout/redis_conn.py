import redis


class RedisConnection:
    def conn(self) -> redis.Redis:
        host = "redis"
        port = 6379
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn
