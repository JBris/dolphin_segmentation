import redis

#Wrapper class for the Redis cache.
class Cache:

    def __init__(self):
        self.cache = redis.Redis(host='redis', port=6379)


    def inc(self, key):
        return self.cache.inc(key)
