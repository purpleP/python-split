"""Functions to split or partition sequences."""

from collections import defaultdict, deque, OrderedDict
from functools import partial
from itertools import count, islice, tee, zip_longest, chain, takewhile
from operator import eq, itemgetter
from six import iteritems as items


__all__ = ['chunks', 'concat', 'groupby', 'partition', 'split']
__author__ = 'Michael Doronin'
__license__ = 'MIT'
__version__ = '1.0'


def groupby(sequence, key=lambda x: x):
    """
    Takes a sequence and lazily return equivalence classes with their
    identifier except instead of sets returns sequence (may have duplicates)

    Arguments:

    same as itertools.groupby except key is by default identity function
    which makes this function return groups of identical elements in sequence

    >>> [(k, list(i)) for k,i in groupby(lambda x: x%3, range(7))]
    [(0, [0, 3, 6]), (1, [1, 4]), (2, [2, 5])]

    """
    buffers = defaultdict(deque)
    kvs = ((key(item), item) for item in sequence)
    seen_keys = set()
    def subseq(buffered):
        while True:
            if buffered:
                yield buffered.popleft()
            else:
                next_key, value = next(kvs)
                buffers[next_key].append(value)
    while True:
        try:
            k, value = next(kvs)
        except StopIteration:
            for bk, group in items(buffers):
                if group and bk not in seen_keys:
                    yield (bk, group)
            return
        else:
            buffers[k].append(value)
            if k not in seen_keys:
                seen_keys.add(k)
                yield k, subseq(buffers[k])


def partition(condition, sequence):
    """
    Split a sequence into two subsequences, in single-pass and preserving order.

    Arguments:

    condition   a function; if condition is None, split true and false items
    sequence    an iterable object

    Return a pair of generators (seq_true, seq_false). The first one
    builds a subsequence for which the condition holds, the second one
    builds a subsequence for which the condition doesn't hold.

    As the function works in single pass, it leads to build-up of both
    subsequences even if only one of them is consumed.

    It is similar to Data.List.partition in Haskell, or running two
    complementary filters:

       from itertools import ifilter, ifilterfalse
       (ifilter(condition, sequence), ifilterfalse(condition, sequence))

    >>> def odd(x): return x%2 != 0
    >>> odds, evens = partition(odd, range(10))
    >>> next(odds)
    1
    >>> next(odds)
    3
    >>> list(evens)
    [0, 2, 4, 6, 8]
    >>> list(odds)
    [5, 7, 9]

    >>> class IsOdd(object): # objects with overloaded bool()
    ...     def __init__(self, x):
    ...         self.x = x
    ...     def __bool__(self):     # Python 3
    ...         return self.x % 2 != 0
    ...     def __nonzero__(self):  # Python 2
    ...         return self.x % 2 != 0
    ...
    >>> odds, evens = partition(lambda v: IsOdd(v), range(3))
    >>> list(odds)
    [1]
    >>> list(evens)
    [0, 2]

    """
    a, b = tee((condition(i), i) for i in sequence)
    return (
        (i for pred_value, i in a if pred_value),
        (i for pred_value, i in b if not pred_value),
    )


def chunks(sequence, n, fillvalue=None):
    """
    Split a sequence into chunks of size n.
    Return an iterator over chunks.

    Arguments:

    sequence    an iterable object
    n           chunk size
    fillvalue   value would be used to fill not enough values have been in iterator

    This function is lazy and produces new chunks only on demand:

    """
    assert n >= 1, "chunk size is not positive"
    return zip_longest(*((iter(sequence),) * n), fillvalue=fillvalue)


def split(delimiter, sequence):
    """
    Break a sequence on particular elements.
    Return an iterator over chunks.

    Arguments:

    delimiter   if a function, it returns True on chunk separators;
                otherwise, it is the value of chunk separator.
    sequence    original sequence;

    """
    delimiter = delimiter if callable(delimiter) else partial(eq, delimiter)
    sequence = iter(sequence)
    active = OrderedDict()
    id = 0
    def append_to_first_buffer(item):
        buff = next(iter(active.values()))
        buff.append(item)
    def subgen(id):
        buffered = active[id]
        while True:
            if buffered:
                for i in range(len(buffered)):
                    yield buffered.popleft()
            elif id not in active:
                return
            else:
                try:
                    item = next(sequence)
                except StopIteration:
                    active.pop(id)
                    return
                else:
                    if delimiter(item):
                        if active:
                            active.popitem(last=False)
                    else:
                        if active:
                            append_to_first_buffer(item)
                        else:
                            yield item
    while True:
        try:
            item = next(sequence)
        except StopIteration:
            if not id:
                active[1] = deque()
                yield subgen(1)
            return 
        else:
            if delimiter(item):
                if active:
                    active.popitem(last=False)
                buffer = deque()
                id += 1
                subg = subgen(id)
                active[id] = buffer
                yield subg
            else:
                if active:
                    append_to_first_buffer(item)
                else:
                    buffer = deque([item])
                    id += 1
                    subg = subgen(id)
                    active[id] = buffer
                    yield subg

def concat(seq, *seqs):
    return chain(seq, *seqs) if seqs else chain.from_iterable(seq)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
