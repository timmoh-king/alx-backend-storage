#!/usr/bin/env python3

"""
    Create a Cache class. In the __init__ method
    store an instance of the Redis client as a private variable named _redis
    (using redis.Redis()) and flush the instance using flushdb.
"""

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def call_history(method: Callable):
    """define a call_history decorator that takes a callable arg"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
            stores methods and return args and output
        """
        inputs = '{}:inputs'.format(method.__qualname__)
        outputs = '{}:outputs'.format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
        method_return = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, method_return)

        return method_return
    return wrapper


def count_calls(method: Callable):
    """define a count_calls decorator that takes a single"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"call_count:{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """define class attributes"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.call_count = 0
        self.inputs = []
        self.outputs = []

    def total_calls(self):
        """return the call count"""
        return self.call_count

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method that takes a data argument and returns a string"""
        self.call_count += 1

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
