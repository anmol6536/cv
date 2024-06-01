from typing import Iterable, Sized, Union
from pathlib import Path
from PIL import Image
from uuid import uuid4


def yielder(data: Union[Iterable, Sized], n: int):
    """
    Yield n elements at a time from data
    :param data: Iterable or Sized
    :param n: int
    :return: Iterable
    """
    for i in range(0, len(data), n):
        yield data[i:i + n]


def sanitize_jpegs(folder: Path, subset: list[str] = (".jpg", )):
    files = [i for i in folder.iterdir() if i.is_file() and (i.suffix.lower() in subset)]
    directories = [i for i in folder.iterdir() if i.is_dir()]

    for file in files:
        image = Image.open(file.__str__())
        image.save(file.parent / f"{uuid4()}.jpg", dpi=(150, 150))
        file.unlink(missing_ok=True)
    for dir in directories:
        sanitize_jpegs(dir, subset)