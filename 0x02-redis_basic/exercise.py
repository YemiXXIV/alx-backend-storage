#!/usr/bin/env python3
"""
To write to redis
"""
import redis
from uuid import uuid4
from typing import Union


class Cache():
    """
    write to redis
    """
    def __init__(self) -> None:
        """
        initialize redis in class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        get uuid key and save data
        """
        keystore = str(uuid4())
        self._redis.set(keystore, data)
        return keystore
