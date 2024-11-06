import json
import sys

from src.config import STOCKFISH, load_config
from src.puzzle.puzzle_manager import download_puzzles

if len(sys.argv) < 2:
    print("USAGE:")
    print("py setup.py stockfish STOCKFISH_PATH")
    print("py setup.py uci ENGINE_NAME ENGINE_PATH")
    print("py setup.py puzzles")
    print("py setup.py option ENGINE_NAME KEY [VALUE]")
    exit(1)

command = sys.argv[1]
tokens = sys.argv[2:]
config = load_config()
if command == "uci":
    if len(tokens) < 2:
        print("USAGE: py setup.py uci ENGINE_NAME ENGINE_PATH")
        exit(2)
    config[tokens[0]] = {}
    config[tokens[0]]["path"] = tokens[1]

if command == "stockfish":
    if len(tokens) < 1:
        print("USAGE: py setup.py stockfish STOCKFISH_PATH")
        exit(3)
    config[STOCKFISH] = {}
    config[STOCKFISH]["path"] = tokens[0]

if command == "puzzles":
    download_puzzles()

if command == "option":
    if len(tokens) < 2:
        print("py setup.py option ENGINE_NAME KEY [VALUE]")
        exit(-1)
    value = ""
    if len(tokens) > 2:
        value = tokens[2]
    config[tokens[0]][tokens[1]] = value

f = open("config.json", "w")
f.write(json.dumps(config))
f.close()
