#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
from functools import lru_cache


@lru_cache(512)
def fib(n):    # serie de Fibonacci hasta n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result


if __name__ == "__main__":
    print(fib(int(sys.argv[1])))
