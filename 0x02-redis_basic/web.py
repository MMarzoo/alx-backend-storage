#!/usr/bin/env python3
'''
Caching request module
'''

import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    ''' Decorator for get_page '''
    @wraps(fn)
    def wrapper(url: str) -> str:
        ''' wrapper function '''
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    ''' Function to get page '''
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'

    print(get_page(url))
    print(get_page(url))
