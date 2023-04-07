import os
import re
from typing import Iterable, List, Optional, Callable, Any, Iterator

def filter_query(value: str, data: Iterable[str]) -> Iterator[str]:
    return filter(lambda l: value in l, data)

def regex_query(value: str, data: Iterable[str]) -> Iterator[str]:
    regexp: re.Pattern = re.compile(value)
    return filter(lambda x: re.search(regexp, x), data)

def map_query(value: str, data: Iterable[str]) -> Iterator[str]:
    return map(lambda l: l.split(' ')[int(value)], data)


def unique_query(data: Iterable[str], *args: Any, **kwargs: Any) -> set[str]:
    return set(data)


def sort_query(value: str, data: Iterable[str]) -> List[str]:
    if value == 'desc':
        reverse: bool = True
    else:
        reverse = False
    return sorted(data, reverse=reverse)


def limit_query(value: str, data: Iterable[str]) -> List[str]:
    return list(data)[:int(value)]


def read_file(filename: str) -> Iterable[str]:
    with open(filename) as file:
        for line in file:
            yield line


dict_comm_to_function: dict[str, Callable] = {
    'filter': filter_query,
    'regex': regex_query,
    'map': map_query,
    'unique': unique_query,
    'sort': sort_query,
    'limit': limit_query
}


def create_query(filename: str, cmd: str, value: str, data: Optional[Iterable[str]]) -> List[str]:
    if data is None:
        data_to_proceed: Iterable[str] = read_file(filename)
    else:
        data_to_proceed = data

    function = dict_comm_to_function[cmd]
    res = function(value=value, data=data_to_proceed)

    return list(res)