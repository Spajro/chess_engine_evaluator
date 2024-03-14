import pathlib
import urllib.request

import zstandard

from src.puzzle import Puzzle


def load(k: int) -> [Puzzle]:
    f = open("lichess_db_puzzle.csv")
    f.readline()
    result = []
    for i in range(k):
        result.append(Puzzle(f.readline()))
    return result


def download_puzzles():
    path = __download("https://database.lichess.org/lichess_db_puzzle.csv.zst", "lichess_db_puzzle.csv.zst")
    __unpack(path, "lichess_db_puzzle.csv")
    __remove("lichess_db_puzzle.csv.zst")


def __download(url: str, name: str) -> str:
    path, _ = urllib.request.urlretrieve(url, name)
    return path


def __unpack(path: str, name: str):
    input_file = pathlib.Path(path)
    with open(input_file, 'rb') as compressed:
        decomp = zstandard.ZstdDecompressor()
        output_path = pathlib.Path(".") / name
        with open(output_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)


def __remove(path: str):
    pathlib.Path.unlink(pathlib.Path(path))
