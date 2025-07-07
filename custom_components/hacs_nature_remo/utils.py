"""Some utility functions"""

from typing import Any
from typing import Iterable
from typing import TypeVar

T = TypeVar("T")


def find_by(items: Iterable[T], attr: str, value: Any = None) -> T:
    """Find item in items that attribute key and attribute"""
    for x in items:
        if hasattr(x, attr) and getattr(x, attr) == value:
            return x
    else:
        x = None


def get_keys(items: Iterable[T], attr: str, value: Any = None) -> T:
    """Find item in items that attribute key and attribute"""
    for x in items:
        if hasattr(x, attr) and getattr(x, attr) == value:
            return x
    else:
        x = None
