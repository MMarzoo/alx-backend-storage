#!/usr/bin/env python3
'''
A module for using the Redis NoSQL data storage.
'''

from typing import Callable, Optional, Union
from functools import wraps
from uuid import uuid4
import redis


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

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        '''  Gets key's value from redis and converts '''
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """Get the value from the Redis database as string"""
        value = self._redis.get(key)
        return value.decode("utf-8") if value else "(nil)"

    def get_int(self, key: str) -> int:
        """Get the value from the Redis database as integer"""
        value = self._redis.get(key)
        return int(value.decode("utf-8")) if value else 0
