import concurrent.futures
from typing import Tuple, Optional

from src.engines import Engine
from src.flags import get_threads
from src.templates import EngineTemplate

threads = get_threads()


class Puzzle:
    def __init__(self, row: str):
        fields = row.split(',')
        self.fen = fields[1]
        self.moves = fields[2].split(" ")

    def __str__(self):
        return "{" + self.fen + ",moves[" + ",".join(self.moves) + "]}"


def solve_puzzle(engine: Engine, puzzle: Puzzle) -> Tuple[bool, 'Puzzle', Optional[list[str]]]:
    engine.update_fen(puzzle.fen, [puzzle.moves[0]])
    move_time = 10 * 1000
    moves = [puzzle.moves[0]]
    i = 1
    while i < len(puzzle.moves):
        move = engine.make_move(move_time, move_time)
        moves.append(move)
        if move != puzzle.moves[i]:
            engine.quit()
            return False, puzzle, moves
        i += 1
        if i == len(puzzle.moves):
            engine.quit()
            return True, puzzle, None
        engine.update([puzzle.moves[i]])
        i += 1
    print("ERROR")
    engine.quit()
    return False, puzzle, moves


def solve_puzzles(engine: EngineTemplate, puzzles: [Puzzle]):
    data = [(engine.get_instance(), puzzle) for puzzle in puzzles]
    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        futures = [executor.submit(solve_puzzle, e, p) for e, p in data]
    return [f.result() for f in futures]
