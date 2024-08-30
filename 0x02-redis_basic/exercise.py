#!/usr/bin/env python3
"""
To write to redis
"""
import redis
from uuid import uuid4
from typing import Union, cast, Optional, TypeVar, Callable
from functools import wraps

T = TypeVar('T', str, bytes, int, float, None)
UnionOfTypes = Union[str, bytes, int, float, None]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count of method calls 
        and returns the original method result
        """
        key = method.__qualname__
        self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result
    return wrapper

def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and outputs 
        for a method in Redis
        """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output
        """
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"
        self._redis.rpush(key_inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, str(output))
        return output

    return wrapper

    
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

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        get uuid key and save data
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[
            Callable] = None) -> Optional[T]:
        """
        Retrieve data from Redis and
        optionally apply a conversion function.
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return cast(T, data)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis
        and convert it to a string.
        """

        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and
        convert it to an integer.
        """
        return self.get(key, fn=int)


def replay(method: Callable):
    """
    Display the history of calls for/to
    a particular function/method.
    """
    key_inputs = f"{method.__qualname__}:inputs"
    key_outputs = f"{method.__qualname__}:outputs"

    redis_instance = method.__self__._redis
    inputs = redis_instance.lrange(key_inputs, 0, -1)
    outputs = redis_instance.lrange(key_outputs, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode('utf-8')
        output_str = output_data.decode('utf-8')
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")
