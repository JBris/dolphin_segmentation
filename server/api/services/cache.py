import redis
import time

#Wrapper class for the Redis cache.
class Cache:

    def __init__(self):
        self.cache = redis.Redis(host='redis', port=6379)

    def incr(self, key):
        while True:
            try: return self.cache.incr(key)
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)
        
