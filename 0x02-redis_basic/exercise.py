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
