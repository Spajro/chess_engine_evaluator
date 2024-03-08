from src.puzzle import Puzzle


def load(k: int) -> [Puzzle]:
    f = open("lichess_db_puzzle.csv")
    f.readline()
    result = []
    for i in range(k):
        result.append(Puzzle(f.readline()))
    return result
