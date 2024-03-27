#!/usr/bin/env python3
"""
This module provides a caching system using Redis.
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls made to the cache"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input = str(args)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{method.__qualname__}:inputs", input)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a particular function"""
    instance = fn.__self__
    inputs = instance._redis.lrange(f"{fn.__qualname__}:inputs", 0, -1)
    outputs = instance._redis.lrange(f"{fn.__qualname__}:outputs", 0, -1)

    print(f"{fn.__qualname__} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        print(f"{fn.__qualname__}{input.decode('utf-8')} -> {output.decode('utf-8')}")


class Cache:
    """Cache class to interface with the Redis key-value store"""

    def __init__(self):
        """Initialize Redis, flush existing data and save instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache using a random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get data from the cache and convert it back to the desired format"""
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Get data from the cache as a UTF-8 decoded string"""
        value = self.get(key)
        return value.decode('utf-8') if value else value

    def get_int(self, key: str) -> int:
        """Get data from the cache as an integer"""
        value = self.get(key)
        return int(value) if value and value.isdigit() else 0
