import pathlib
import urllib.request

import zstandard

from src.puzzle.puzzle import Puzzle


def load(k: int, mates=True) -> [Puzzle]:
    f = open("lichess_db_puzzle.csv")
    f.readline()
    result = []
    i = 0
    while i < k:
        puzzle = Puzzle(f.readline())
        if 'mate' in puzzle.tags and not mates:
            continue
        result.append(puzzle)
        i += 1
    f.close()
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
        output_path = pathlib.Path("..") / name
        with open(output_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)
            destination.close()
        compressed.close()


def __remove(path: str):
    pathlib.Path.unlink(pathlib.Path(path))
