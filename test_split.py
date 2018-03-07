from itertools import chain, repeat

from hypothesis import given

import hypothesis.strategies as st
import pytest


from split import chunks, groupby, partition, split


expected_keys = (1, 2, 3, 4, 5)
expected_groups = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


def call(*args, **kwargs):
    return args, kwargs


@pytest.fixture()
def data():
    return chain.from_iterable(repeat(expected_keys, 2))


def test_groupby_keys(data):
    assert expected_keys == tuple(key for key, group in groupby(data))


def test_groupby_values(data):
    assert expected_groups == tuple(tuple(group) for key, group in groupby(data))


def test_partition():
    expected = (1, 3, 5, 7, 9), (0, 2, 4, 6, 8)
    assert expected == tuple(map(tuple, partition(lambda x: x % 2 != 0, range(10))))



@given(st.text())
def test_split(s):
    assert list(map(''.join, split('a', s))) == s.split('a')


@pytest.mark.parametrize(
    'call,expected',
    (
        (call(range(10), 3), [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]),
    )
)
def test_chunks(call, expected):
    args, kwargs = call
    assert expected == list(chunks(*args, **kwargs))
