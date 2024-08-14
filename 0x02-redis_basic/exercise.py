#!/usr/bin/env python3
'''
A module for using the Redis NoSQL data storage.
'''

from typing import Callable, Optional, Union, Any
from functools import wraps
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """ Count how many times methods of the Cache class are called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increment every time the method is called """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    ''' Caching class '''
    def __init__(self) -> None:
        ''' Initialize new cache object '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    #@call_history
    #@count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' Stores data in redis with randomly generated key '''
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        '''  Gets key's value from redis and converts '''
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """ Converts bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converts bytes to integers
        """
        return int(data)
