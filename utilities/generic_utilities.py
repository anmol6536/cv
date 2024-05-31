from typing import Iterable, Sized, Union


def yielder(data: Union[Iterable, Sized], n: int):
    """
    Yield n elements at a time from data
    :param data: Iterable or Sized
    :param n: int
    :return: Iterable
    """
    for i in range(0, len(data), n):
        yield data[i:i + n]
