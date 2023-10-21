#!/usr/bin/env python3

"""
    Create a Cache class. In the __init__ method
    store an instance of the Redis client as a private variable named _redis
    (using redis.Redis()) and flush the instance using flushdb.
"""

import redis
import uuid
from typing import Union, Callable


class Cache:
    """define class attributes"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
             The callable will be used to convert the data back to the desired form
        """
        data = self._redis.get(key)

        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_int(self):
        """
            automatically parametrize Cache.get with the correct conversion fn
        """
        return self.get(key, fn = lambda x: int(x) if x is not None else None)

    def get_str(self):
        """
            automatically parametrize Cache.get with the correct conversion fn
        """
        return self.get(key, fn = lambda x: x.decode('utf-8'))
