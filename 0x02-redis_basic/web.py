#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable

cache = redis.Redis(host='localhost', port=6379, db=0)


# Decorator for caching and counting accesses
def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Cache key for the HTML content and access count
        cache_key = f"content:{url}"
        count_key = f"count:{url}"

        # Check if the page is in the cache
        cached_page = cache.get(cache_key)
        if cached_page:
            print("Cache hit")
            # Increment the access count in Redis
            cache.incr(count_key)
            return cached_page.decode('utf-8')

        # If not cached, fetch the page
        print("Cache miss")
        result = func(url)

        # Cache the result with an expiration time of 10 seconds
        cache.setex(cache_key, 10, result)

        # Increment the access count
        cache.incr(count_key)

        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"

    print(get_page(url))
    print(get_page(url))
