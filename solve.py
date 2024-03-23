import sys

from src.puzzle.length_stats import LengthStats
from src.puzzle.puzzle import solve_puzzles
from src.puzzle.puzzle_manager import load
from src.puzzle.tag_stats import TagStats
from src.templates import UciEngineTemplate

if len(sys.argv) < 2:
    print("SYNTAX: py solve.py ENGINE PUZZLES_COUNT")
    exit(200)

tag_stats = TagStats()
length_stats = LengthStats()

k = int(sys.argv[2])
puzzles = load(k)
result = solve_puzzles(UciEngineTemplate(sys.argv[1]), puzzles)

score = 0
failed = []

for solved, puzzle, optional_moves in result:
    tag_stats.add_puzzle(solved, puzzle)
    length_stats.add_puzzle(solved, puzzle)
    if solved:
        score += 1
    else:
        failed.append(puzzle.__str__() + " | [" + ",".join(optional_moves) + "]")

print("RESULT: " + str(score) + "/" + str(k))
print("FAILED: ")
print('\n'.join(failed))
print("STATS FOR TAG:")
print(tag_stats)
print("STATS FOR LENGTH:")
print(length_stats)
