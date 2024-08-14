#!/usr/bin/env python3
'''
Caching request module
'''
import redis
import requests
from functools import wraps
from typing import Callable

client = redis.Redis()


def track_get_page(fn: Callable) -> Callable:
    ''' Decorator for get_page '''
    @wraps(fn)
    def wrapper(url: str) -> str:
        ''' wrapper function '''
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
             print("Cache hit")
             return cached_page.decode('utf-8')

        print("Cache miss")
        response = fn(url)
        client.setex(f'{url}', 10, response)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    ''' Function to get page '''
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'

    print(get_page(url))
    print(get_page(url))
