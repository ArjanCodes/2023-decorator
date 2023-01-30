"""
One downside of using decorators is that they don't play nice with type checkers by default.

In `decorator_functools_wrap.py`, the typing system thinks the signature of `count_prime_numbers` is:

> Callable[..., Any]

However, we can help the type checker out by using some generics available in the typing library:
- [TypeVar](https://docs.python.org/3/library/typing.html#typing.TypeVar)
- [ParamSpec](https://docs.python.org/3/library/typing.html#typing.ParamSpec)

ParamSpec is available since 3.10, but is also available in the `typing-extensions` library.

This also helps check to make sure that your original signature doesn't change, like in the `hydra` example you mentioned; the type checker would raise a warning.
"""

import functools
import logging
from math import sqrt
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

# First, create the generic types
# TypeVar represents a single value
WrappedReturn = TypeVar("WrappedReturn")
# ParamSpec represents args and kwargs of a function signature
WrappedParams = ParamSpec("WrappedParams")

# Change the decorator definitions to reflect the generic types
def with_logging(
    func: Callable[WrappedParams, WrappedReturn]
) -> Callable[WrappedParams, WrappedReturn]:
    @functools.wraps(func)
    # Assign generic types to the args and kwargs
    def wrapper(*args: WrappedParams.args, **kwargs: WrappedParams.kwargs) -> WrappedReturn:
        logging.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return value

    return wrapper


# Same changes here
def benchmark(
    func: Callable[WrappedParams, WrappedReturn]
) -> Callable[WrappedParams, WrappedReturn]:
    @functools.wraps(func)
    def wrapper(*args: WrappedParams.args, **kwargs: WrappedParams.kwargs) -> WrappedReturn:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f"Execution of {func.__name__} took {run_time:.2f} seconds.")
        return value

    return wrapper


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for element in range(2, int(sqrt(number)) + 1):
        if number % element == 0:
            return False
    return True


@with_logging
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count += 1
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    # The type checker will reflect the correct signature: Callable[int, int]
    count_prime_numbers(50000)


if __name__ == "__main__":
    main()
