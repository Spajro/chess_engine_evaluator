import concurrent
import sys

from src.flags import summarize, get_threads
from src.puzzle.puzzle import Puzzle
from src.puzzle.puzzle_manager import load
from src.templates import UciEngineTemplate, StockfishEngineTemplate, EngineTemplate

print(summarize())
if len(sys.argv) < 2:
    print("SYNTAX: py test_eval.py ENGINE TEST_LENGTH")
    exit(200)

k = int(sys.argv[2])
puzzles = load(k, mates=False)
engine = UciEngineTemplate(sys.argv[1])
stockfish = StockfishEngineTemplate(2500)


def evaluate(engine_template: EngineTemplate,
             stockfish_template: EngineTemplate,
             puzzle: Puzzle) -> (float, float, float, float):
    engine = engine_template.get_instance()
    stockfish = stockfish_template.get_instance()

    engine.update_fen(puzzle.fen, [])
    stockfish.update_fen(puzzle.fen, [])
    re1 = engine.eval()
    rs1 = stockfish.eval()

    engine.update_fen(puzzle.fen, [puzzle.moves[0]])
    stockfish.update_fen(puzzle.fen, [puzzle.moves[0]])
    re2 = engine.eval()
    rs2 = stockfish.eval()

    engine.quit()
    stockfish.quit()
    return re1, re2, rs1, rs2


with concurrent.futures.ThreadPoolExecutor(get_threads()) as executor:
    futures = [executor.submit(evaluate, engine, stockfish, puzzle) for puzzle in puzzles]

result = [f.result() for f in futures]
engine_result = []
stockfish_result = []
for e1, e2, s1, s2 in result:
    engine_result.append(e1)
    engine_result.append(e2)
    stockfish_result.append(s1)
    stockfish_result.append(s2)

result = 0.0
for i in range(k):
    result += abs(engine_result[i] - stockfish_result[i])
print(k, len(stockfish_result))
print("Evaluation mean absolute error: ", result / (2 * k))
