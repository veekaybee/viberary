from redis import Redis


class Cache():
    
    def redis_connection(self) -> Redis:
        host = "localhost"
        port = 6379
        redis_conn = Redis(host=host, port=port)
        return redis_conn