import redis
import time

#Wrapper class for the Redis cache.
class Cache:
    def __init__(self):
        self.cache = redis.Redis(host='redis', port=6379)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value, ex = None):
        return self.cache.set(key, value, ex)
        