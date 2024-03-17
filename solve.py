import sys

from src.puzzle import solve_puzzles
from src.puzzle.puzzle_manager import load
from src.puzzle.tag_stats import TagStats
from src.templates import UciEngineTemplate

if len(sys.argv) < 2:
    print("SYNTAX: solve.py ENGINE PUZZLES_COUNT")
    exit(200)

k = int(sys.argv[2])
puzzles = load(k)
result = solve_puzzles(UciEngineTemplate(sys.argv[1]), puzzles)
score = 0
tag_stats = TagStats()

print("FAILED: ")
for solved, puzzle, optional_moves in result:
    if solved:
        score += 1
        tag_stats.add_puzzle(True, puzzle)
    else:
        tag_stats.add_puzzle(False, puzzle)
        print(puzzle.__str__() + " | [" + ",".join(optional_moves) + "]")

print("RESULT: " + str(score) + "/" + str(k))
print("STATS FOR TAG:")
print(tag_stats)
