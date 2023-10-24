#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage.
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """Decorator Function to Count Calls
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Wrapper function to call and count method passed
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Call History Decorator Function.
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Stores Method returns and arguments and returns its output.
        """
        inputs = '{}:inputs'.format(method.__qualname__)
        outputs = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
        method_return = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, method_return)
        return method_return
    return invoker


def replay(fn: Callable) -> None:
    """Displays the call history.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    function_name = fn.__qualname__
    inputs = '{}:inputs'.format(function_name)
    outputs = '{}:outputs'.format(function_name)
    function_call_count = 0
    if redis_store.exists(function_name) != 0:
        function_call_count = int(redis_store.get(function_name))
    print('{} was called {} times:'.format(function_name, function_call_count))
    function_inputs = redis_store.lrange(inputs, 0, -1)
    function_outputs = redis_store.lrange(outputs, 0, -1)
    for function_input, function_output in zip(
            function_inputs,
            function_outputs):
        print('{}(*{}) -> {}'.format(
            function_name,
            function_input.decode("utf-8"),
            function_output,
        ))


class Cache:
    """Object to help in adding data in a Redis storage.
    """

    def __init__(self) -> None:
        """Initializes Cache class instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Adds a value in a Redis returning the storage key.
        """
        storage_key = str(uuid.uuid4())
        self._redis.set(storage_key, data)
        return storage_key

    def get(
            self,
            key: str,
            fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis storage.
        """
        stored_data = self._redis.get(key)
        return fn(stored_data) if fn is not None else stored_data

    def get_str(self, key: str) -> str:
        """Retrieves string from a Redis storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer from a Redis storage.
        """
        return self.get(key, lambda x: int(x))
