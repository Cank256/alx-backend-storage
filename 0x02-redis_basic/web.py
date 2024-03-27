#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps

r = redis.Redis()
EXPIRE_TIME = 10


def count_requests(method: Callable) -> Callable:
    """ Count how many times URLs are accessed """
    @wraps(method)
    def wrapper(url):
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Get the HTML content of the specified URL """
    cached_html = r.get(f"cached:{url}")
    if cached_html:
        return cached_html.decode('utf-8')

    html = requests.get(url).text
    r.setex(f"cached:{url}", EXPIRE_TIME, html)
    return html
